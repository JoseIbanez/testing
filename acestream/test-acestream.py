#!/usr/bin/env python3
import argparse
import requests
import json
import time
import os.path
import re
from pathlib import Path
import subprocess


def get_stat_url(port,id):

    #print(port,id)

    api_url = f"http://127.0.0.1:{port}/ace/getstream?id={id}&format=json"

    try:
        response = requests.get(api_url)
        result = response.json()
        resp = result.get('response')
        stat_url = resp.get('stat_url')
        #print(stat_url)

    except:
        return None


    return stat_url



def get_stat(stat_url,port):

    if not stat_url:
        stat={ 'port': port,
                'status': None
            }
        return stat

    response = requests.get(stat_url)
    result = response.json()
    #print(result)

    resp = result.get('response')
    if not resp:
        return None

    #print(resp)
    stat = {
        'port': port,
        'status': resp.get('status'),
        'peers': resp.get('peers'),
        'speed_down': resp.get('speed_down'),
        'speed_up': resp.get('speed_up'),
        'last_ts': resp.get('livepos',{}).get('last_ts')
    }

    return stat



def get_id_from_folder(port):


    with open(f"/mnt/d1/hls/{port}/id", 'r') as file:
        id = file.read().rstrip()

    return id


def get_age_m3u8(port):


    path=f"/mnt/d1/hls/{port}/stream.m3u8"

    try:
        age = int(time.time() - os.path.getmtime(path))
    except:
        age = None

    return age


def check_docker_logs(port):

    process = subprocess.Popen(['docker', 'logs', '--tail' ,'10', f'acelink.{port}'],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    ts=None
    speed=None

    #print(stdout)
    #print(stderr)
    result_lines = stderr.decode('utf-8').split('\n')

    for line in result_lines:

        m = re.search(r"stream(\d+)\.ts",line)
        if m:
            ts=m.group(1)

        m = re.search(r"speed= *([\d\.]+)x",line)
        if m:
            speed=m.group(1) 

    return ts,speed



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", help="acestream port", default=6878, type=int)
    parser.add_argument("--duration", help="acestream port", default=1000, type=int)
    args = parser.parse_args()

    port = args.port
    duration = args.duration

    if port==0:
        check_all()
        return


    check_port(port,duration)



def check_port(port,duration):

    id = get_id_from_folder(port)

    stat_url = get_stat_url(port,id)

    for i in range(duration):
        stat = get_stat(stat_url,port)
        age = get_age_m3u8(port)
        ts,speed = check_docker_logs(port)

        if stat:
            stat['age']=age
            stat['ts']=ts
            stat['speed']=speed


        print(stat)
        time.sleep(2)
    




def check_all():


    for path in Path('/mnt/d1/hls').rglob('id'):
        m = re.search(r'.*/hls/(.+)/id',str(path))
        port = int(m.group(1)) if m else None


        id = get_id_from_folder(port)
        stat_url = get_stat_url(port,id)

        stat = get_stat(stat_url,port)
        age = get_age_m3u8(port)
        ts,speed = check_docker_logs(port)

        if stat:
            stat['age']=age
            stat['ts']=ts
            stat['speed']=speed

        print(stat)




if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import requests
import json
import time
import os.path
import re
from pathlib import Path


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

    if port == 6878:
        port = 3231

    with open(f"/mnt/d1/hls/{port}/id", 'r') as file:
        id = file.read().rstrip()

    return id

def get_age_m3u8(port):


    if port == 6878:
        port = 3231

    path=f"/mnt/d1/hls/{port}/stream.m3u8"

    try:
        age = int(time.time() - os.path.getmtime(path))
    except:
        age = None

    return age



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

        if stat:
            stat['age']=age

        print(stat)
        time.sleep(2)
    

def check_all():


    for path in Path('/mnt/d1/hls').rglob('id'):
        m = re.search(r'.*/hls/(.+)/id',str(path))
        port = int(m.group(1)) if m else None


        if port == 3231:
            port = 6878


        id = get_id_from_folder(port)
        stat_url = get_stat_url(port,id)

        stat = get_stat(stat_url,port)
        age = get_age_m3u8(port)

        if stat:
            stat['age']=age

        print(stat)




if __name__ == "__main__":
    main()

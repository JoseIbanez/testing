#!/usr/bin/env python3
import argparse
import requests
import json
import time


def get_stat_url(port,id):

    print(port,id)

    api_url = f"http://127.0.0.1:{port}/ace/getstream?id={id}&format=json"

    response = requests.get(api_url)
    result = response.json()

    resp = result.get('response')
    if not resp:
        return None

    stat_url = resp.get('stat_url')
    print(stat_url)
    return stat_url



def get_stat(stat_url):

    if not stat_url:
        return None

    response = requests.get(stat_url)
    result = response.json()
    #print(result)

    resp = result.get('response')
    if not resp:
        return None

    #print(resp)
    stat = {
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





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="acestream id", default=None)
    parser.add_argument("-p","--port", help="acestream port", default=6878, type=int)
    parser.add_argument("--duration", help="acestream port", default=1000, type=int)
    args = parser.parse_args()

    port = args.port
    id   = args.id
    duration = args.duration

    if not id:
        id = get_id_from_folder(port)

    stat_url = get_stat_url(port,id)

    for i in range(duration):
        stat = get_stat(stat_url)
        print(stat)
        time.sleep(2)
    


if __name__ == "__main__":
    main()

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

    stat = {
        'status': resp.get('status'),
        'peers': resp.get('peers'),
        'downloaded': resp.get('downloaded')
    }

    return stat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="acestream id")
    parser.add_argument("--port", help="acestream port", default=6878)
    args = parser.parse_args()

    stat_url = get_stat_url(args.port,args.id)

    while True:
        stat = get_stat(stat_url)
        print(stat)
        time.sleep(5)
    


if __name__ == "__main__":
    main()
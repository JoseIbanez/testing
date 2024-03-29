#!/usr/bin/env python3
import requests
from requests.exceptions import HTTPError, ConnectionError
import json
import time
import os.path
import re
from pathlib import Path


def get_stat_url(port,ace_id):

    api_url = f"http://127.0.0.1:{port}/ace/getstream?id={ace_id}&format=json"

    try:
        response = requests.get(api_url)
        result = response.json()
        resp = result.get('response') or {}
        stat_url = resp.get('stat_url')

    except ( HTTPError, ConnectionError ) as e:
        return None


    return stat_url



def get_status(port,ace_id):

    stat_url = get_stat_url(port,ace_id)
    if not stat_url:
        stat={ 'port': port, 'status': None}
        return stat

    response = requests.get(stat_url)
    resp = response.json().get('response')
    if not resp:
        stat={ 'port': port, 'status': None}
        return stat

    stat = {
        'port': port,
        'status': resp.get('status'),
        'peers': resp.get('peers'),
        'speed_down': resp.get('speed_down'),
        'speed_up': resp.get('speed_up'),
        'last_ts': resp.get('livepos',{}).get('last_ts')
    }

    return stat


def get_m3u8_age(port:int):

    path=f"/mnt/d1/hls/{port}/stream.m3u8"
    age = None

    try:
        age = int(time.time() - os.path.getmtime(path))
    except OSError:
        pass

    return age



def list_streams():

    listResult = []

    for path in Path('/mnt/d1/hls').rglob('id'):
        m = re.search(r'.*/hls/(.+)/id',str(path))
        port = int(m.group(1)) if m else None
        ace_id = None
        description = None

        if not port:
            continue

        try:
            with open(f"/mnt/d1/hls/{port}/id","r") as f:
                ace_id = f.readline().rstrip()

            with open(f"/mnt/d1/hls/{port}/description","r") as f:
                description = f.readline().rstrip()

        except OSError as e:
            pass

        if not ace_id:
            continue   

        listResult.append({
            "port": port,
            "ace_id": ace_id,
            "description": description
        })

    return listResult
#!/usr/bin/env python3
import requests
from requests.exceptions import HTTPError, ConnectionError
import json
import time
import os.path
import re
from pathlib import Path

class M3u8Channel:
    ace_id = None
    tvg_id = None
    owner = None
    name = None
    group_title = None

    def __repr__(self):
        return f"{self.tvg_id}:{self.name} ({self.ace_id})"


class M3u8List:

    def __init__(self):
        self.list = []


    def parse_m3u8(self,filename:str):

        tmp_entry = None

        with open(filename,"r",encoding='utf8') as f:
            Lines = f.readlines()


        for line in Lines:

            line = line.rstrip()

            if not line:
                continue

            if line.startswith("#EXTINF:-1"):
                tmp_entry = parse_extinf_line(line)
                continue

            if not tmp_entry:
                continue

            if line.startswith("acestream://"):
                tmp_entry.ace_id = parse_acestream_link(line)

            elif line.startswith("http://"):
                tmp_entry.ace_id = parse_http_link(line)

            else:
                tmp_entry = None
                continue

            if not tmp_entry or not tmp_entry.ace_id:
                continue

            self.list.append(tmp_entry)
            tmp_entry = None

    def seach(self,query):

        ace_id_list = []
        count = 0 
        result = []

        for item in self.list:

            if not item.owner or not "@Lucas" in item.owner: 
                continue

            if item.ace_id in ace_id_list:
                continue

            if (re.search(query, str(item.tvg_id) + str(item.name) )):
                result.append(item)
                ace_id_list.append(item.ace_id)

            if len(result) > 20:
                break



        for item in self.list:

            if len(result) > 20:
                break

            if item.ace_id in ace_id_list:
                continue

            if (re.search(query, str(item.tvg_id) + str(item.name) )):
                result.append(item)
                ace_id_list.append(item.ace_id)



        return result


def parse_extinf_line(line:str): 

    result = M3u8Channel()

    ### get tvg-id
    m = re.search(r'tvg-id="([^"]+)"', line)
    if m:
        result.tvg_id = m.group(1)

    ### get group-title
    m = re.search(r'group-title="([^"]+)"', line)
    if m:
        result.group_title = m.group(1)

    ### owner
    m = re.search(r'(@[\w]+)', line)  if result.group_title else None
    if m:
        result.owner = m.group(1)

    ### name
    m = re.search(r', *(.+)$', line)
    if m:
        result.name = m.group(1).rstrip()



    return result 


def parse_acestream_link(line:str):

    ace_id = None

    ### get ace_id
    m = re.search(r'acestream://([\w]+)', line)
    if m:
        ace_id = m.group(1)

    return ace_id

def parse_http_link(line:str):

    ace_id = None

    ### get ace_id
    m = re.search(r'http://.*getstream.*id=([\w]+)', line)
    if m:
        ace_id = m.group(1)

    return ace_id


def main():
    parse_extinf_line('#EXTINF:-1 tvg-logo="https://i.ibb.co/QfX8Xx6/DAZN3.jpg" group-title="By @Lucas_m_o_o_m" tvg-id="DAZN 3", DAZN 3 1080')
    parse_acestream_link('acestream://50b6d2b5fd59fefb9f4fd2176994d418f2b94a80')
    parse_http_link('http://127.0.0.1:6878/ace/getstream?id=37d42d2b5d2278e6bb5810329a5f220867b3cf0c')

    lista = M3u8List()
    lista.parse_m3u8("/home/ibanez/Projects/testing/zeronet/listas/ramses.m3u8")
    lista.parse_m3u8("/home/ibanez/Projects/testing/zeronet/listas/electroperra.m3u8")
    result = lista.seach("DAZN La")

    print(result)


if __name__ == "__main__":
    main()

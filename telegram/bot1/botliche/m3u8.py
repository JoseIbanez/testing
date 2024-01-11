#!/usr/bin/env python3
import requests
from requests.exceptions import HTTPError, ConnectionError
import json
import time
import os.path
import re
from pathlib import Path
import logging
import itertools

from botliche.config import Config, DATA_PATH

logger = logging.getLogger(__name__)



class M3u8Channel:
    ace_id = None
    tvg_id = None
    owner = None
    name = None
    cname = None
    group_title = None

    def __repr__(self):
        #return f"{self.tvg_id}:{self.name} ({self.ace_id})"
        return f"{self.name} /{self.ace_id}"


class M3u8List:
    """
    Manage m3u8 (ZeroNet) channel lists
    """

    def __init__(self):
        self.list:list[M3u8Channel] = []
        self.config = Config()
        self.sub_list = []


    def load(self):
        self.config.load()

        for item in self.config.get("m3u8_lists"):
            self.parse_m3u8(f"{DATA_PATH}/{item}")

        self.set_cname()


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

        logger.info("Loaded %s, Items:%d",filename,len(self.list))



    def create_sub_list(self):
        """
        """

        self.sub_list = [ (sub_item.get("match") , sub_item.get("replace") )  for sub_item in self.config.get("m3u8_cname",[]) ]

        logger.debug("Subtitution list: %s",self.sub_list)



    def sub_cname(self,channel_name):
        """
        Set common name for a particular channel
        Iterate in subsitution list
        """

        item_name = channel_name
        for sub_item in self.sub_list:
            item_name = re.sub(sub_item[0], sub_item[1], item_name, flags=re.IGNORECASE)

        return item_name


    def set_cname(self):

        self.create_sub_list()

        for item in self.list:
            item.cname = self.sub_cname(item.name)
            logger.info("%s -> %s.",item.name,item.cname)

            
        return None


    def set_cname_old(self):

        for item in self.list:

            item_name = item.name

            item_name = re.sub(' *(1080|720)p?', '', item_name, flags=re.IGNORECASE)
            item_name = re.sub('(4K|1440)p?', 'UHD', item_name, flags=re.IGNORECASE)
            item_name = re.sub('M. LaLiga', 'M+ LaLiga TV', item_name, flags=re.IGNORECASE)
            item_name = re.sub('M.L. Campeones', 'M+ Liga de Campeones', item_name, flags=re.IGNORECASE)
            item.cname = item_name

            logger.info("%s -> %s.",item.name,item.cname)

            
        return None



    def search(self,query):

        result = list(itertools.islice(self.search_iter(query),10))
        return result


    def search_iter(self,query):

        ace_id_list = []
        channel_name = query.replace("+","\+")

        logger.info("Table size %d",len(self.list))

        for item in self.list:

            if not item.owner or not "elcano" in item.owner: 
                continue

            if item.ace_id in ace_id_list:
                continue

            if re.search(channel_name, f"{item.name} {item.cname}", flags=re.IGNORECASE ):
                ace_id_list.append(item.ace_id)
                yield item


        for item in self.list:

            if item.ace_id in ace_id_list:
                continue

            if re.search(channel_name, f"{item.name} {item.cname}", flags=re.IGNORECASE ):
                ace_id_list.append(item.ace_id)
                yield item




    def get_by_id(self, ace_id:str):

        ace_id_list = []
        result = []

        logger.info("Table size %d",len(self.list))

        result = next((item.name for item in self.list if item.ace_id == ace_id), None)
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





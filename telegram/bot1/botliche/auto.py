import logging
import unittest
import logging
import re

from botliche.m3u8 import M3u8List
from botliche.scrape_fetv import EventTVList

logger = logging.getLogger(__name__)

def match_channel():

    events = EventTVList()
    events.get_events()

    lista = M3u8List()
    lista.load()


    m3u8_canon(lista)



    for event in events.list:
        print(event.channels)

        for channel in event.channels:
            channel_name = channel
            result = m3u8_search(lista, channel_name)


            logger.info("Channel:%s -> %s",channel_name,result)


def m3u8_canon(m3u8List:M3u8List):

    for item in m3u8List.list:

        item_name = item.name
        item_name = re.sub(' *(1080|720)', '', item_name)
        item_name = re.sub('M. LaLiga', 'M+ LaLiga TV', item_name)
        item.canon = item_name


        logger.info("%s -> %s.",item.name,item.canon)

        
    return None


def m3u8_search(m3u8List:M3u8List,channel_name:str):


    channel_name = channel_name.replace("+","\+")

    for item in m3u8List.list:

        if re.search(channel_name, item.canon, flags=re.IGNORECASE ):
            return item
        
    return None


import logging
import unittest
import logging
import re

from botliche.m3u8 import M3u8List
from botliche.scrape_fetv import EventTVList

logger = logging.getLogger(__name__)

def match_channel(eventList:EventTVList,aceList:M3u8List):

    messageList = []
 
    for event in eventList.list:
        logger.info("Event:%s",event)

        message = str(event)

        for channel in event.channels:
            channel_name = channel
            result = next(aceList.search_iter(channel_name),None)
            ace_id = f"/{result.ace_id}" if result else ""

            message = message + f"\n- {channel_name} {ace_id}"

        messageList.append(message) 

    return messageList




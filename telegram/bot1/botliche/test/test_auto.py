import logging
import unittest
import logging

from botliche.m3u8 import M3u8List
from botliche.scrape_fetv import EventTVList
from botliche.auto import match_channel
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestScrape(unittest.TestCase):


    def test_match_channel(self):


        eventList = EventTVList()
        eventList.get_events()

        aceList = M3u8List()
        aceList.load()

        result = match_channel(eventList,aceList)

        for event in result:
            logger.info(event)

if __name__ == '__main__':
    unittest.main()

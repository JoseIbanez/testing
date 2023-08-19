import logging
import unittest
import logging


from botliche.m3u8 import M3u8List
from botliche.scrape_fetv import EventTVList
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestScrape(unittest.TestCase):


    def test_get_events(self):

        events = EventTVList()
        print (events.get_events())

        for event in events.list:
            print(event.channels)



if __name__ == '__main__':
    unittest.main()

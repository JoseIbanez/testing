import logging
import unittest
import logging


from botliche.auto import match_channel
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestScrape(unittest.TestCase):


    def test_match_channel(self):

        match_channel()

if __name__ == '__main__':
    unittest.main()

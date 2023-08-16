import logging
import unittest
import logging


from botliche.m3u8 import M3u8List
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestM3u8(unittest.TestCase):


    def test_search(self):

        lista = M3u8List()
        lista.load()
        result = lista.search("laliga")
        print(result)





if __name__ == '__main__':
    unittest.main()

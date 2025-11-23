import logging
import unittest
import logging
import itertools

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

        ace_id = str(result[0]).split("/")[1]
        print(ace_id)
        print(lista.get_by_id(ace_id))


    def test_search_2(self):

        lista = M3u8List()
        lista.load()
        result = list(itertools.islice(lista.search_iter("laliga"),2))
        print(result)


        result = list(lista.search_iter("laaaliga"))
        print(result)


if __name__ == '__main__':
    unittest.main()

import logging
import unittest
import logging


from botliche import fav
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestFav(unittest.TestCase):


    def test_save(self):
        fav.save("hls","3333", 3232, "laliga", 333, "aa")

    def test_search(self):
        fav.save("kill","3333", 3251, "laliga", 333, "aa")
        item = fav.search("3333")
        print(item)

    def test_search_2(self):
        item = fav.search("c373da9e901d414b7384e671112e64d5a2310c29")
        print(item)

if __name__ == '__main__':
    unittest.main()

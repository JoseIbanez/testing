import logging
import unittest

from acelink_server.common import configure_loger
from acelink_server.docker_handler import run_acelink,del_container,get_container
from acelink_server.acestream_test import get_m3u8_age, get_status, list_streams
from acelink_server._version import __version__



logger = logging.getLogger(__name__)

configure_loger()

class TestAcestream(unittest.TestCase):


    def test_list_acestream(self):

        result = list_streams()
        print(result)

if __name__ == '__main__':
    unittest.main()

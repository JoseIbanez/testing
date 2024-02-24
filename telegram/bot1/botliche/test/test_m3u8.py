import logging
import unittest
import logging
import itertools

from botliche.m3u8 import M3u8List
from botliche.m3u8 import parse_acestream_link, parse_extinf_line, parse_http_link
from botliche.common import configure_loger

logger = logging.getLogger(__name__)

configure_loger()

class TestM3u8(unittest.TestCase):


    def test_iter(self):

        lista = M3u8List()
        lista.load()
        result = list(itertools.islice(lista.search_iter("laliga"),2))
        print(result)
        self.assertEqual(len(result),2)


    def test_search(self):
        """
        Test positive search
        """

        lista = M3u8List()
        lista.load()

        query_list = [ "laliga", "DAZN", "Campeones", "Deportes", "Euro" ]

        for query in query_list:

            result = lista.search(query)
            logger.info("query: %s,  result:%s",query,result)
            self.assertGreater(len(result),0)

            ace_id = str(result[0]).split("/")[1]
            self.assertGreater(len(ace_id),10)

            ace_name = lista.get_by_id(ace_id)
            self.assertGreater(len(ace_name),3)

            logger.info("query:%s ace_id:%s channel_name:%s",query,ace_id,ace_name)



    def test_search_negative(self):
        """
        Test negative search
        """

        lista = M3u8List()
        lista.load()

        query_list = [ "laaliga", "DZZN" ]

        for query in query_list:

            result = list(lista.search_iter("query"))
            self.assertEqual(len(result),0)


    def test_parse(self):

        channel = parse_extinf_line('#EXTINF:-1 tvg-logo="https://i.ibb.co/QfX8Xx6/DAZN3.jpg" group-title="By @Lucas_m_o_o_m" tvg-id="DAZN 3", DAZN 3 1080')
        print(channel)
        self.assertEqual(channel.name,"DAZN 3 1080")

        parse_acestream_link('acestream://50b6d2b5fd59fefb9f4fd2176994d418f2b94a80')


        parse_http_link('http://127.0.0.1:6878/ace/getstream?id=37d42d2b5d2278e6bb5810329a5f220867b3cf0c')



    def test_cname(self):

    
        lista = M3u8List()
        lista.config.load()


        lista.create_sub_list()
        input = "M+ Liga de Campeones 3 1080*"
        result = lista.sub_cname(input)

        logger.info(f"{input} -> {result}")


if __name__ == '__main__':
    unittest.main()

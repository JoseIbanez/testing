


import unittest
import json
import logging
from elasticsearch import Elasticsearch

from elastic import get_es_customer_list
from parse import get_customer_list, custumer_details


logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Test_Elastic(unittest.TestCase):

    def test_elastic_00(self):

        resp = get_es_customer_list()

        self.assertIsInstance(resp, dict, "Response should be a list")
        logger.info(json.dumps(resp))


    def test_parse_01(self):

        #load sample data from file
        with open("sample_data/customer_sumary.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        result = get_customer_list(data)
        print(result)

    def test_parse_02(self):

        #load sample data from file
        with open("sample_data/customer_sumary.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        result = custumer_details(data,"DenuVo")
        print(result)



if __name__ == '__main__':
    unittest.main()



import logging
import json
import unittest
from datetime import datetime, date

from finance.yfin.cache import MyDBCache

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = MyDBCache()
        self.ticker = "AAPL"

    def test_fast_info_cache(self):
        """
        Test the MyDBCache class for storing
        and retrieving fast_info data.
        """
        fast_info = self.cache.get_fast_info(self.ticker)
        logger.info("Fast info for %s: %s", self.ticker, json.dumps(fast_info, indent=4))

        # Update the cache with new data
        new_fast_info = {
            "currentPrice": 150.0,
            "yearHigh": 200.0,
            "twoHundredDayAverage": 120.0
        }
        self.cache.put_fast_info(self.ticker, new_fast_info)

        # Retrieve the updated data
        updated_fast_info = self.cache.get_fast_info(self.ticker)
        logger.info("Updated fast info for %s: %s", self.ticker, json.dumps(updated_fast_info, indent=4))

    def test_more_info_cache(self):
        """
        Test the MyDBCache class for storing
        and retrieving more_info data.
        """
        more_info = self.cache.get_more_info(self.ticker)
        logger.info("More info for %s: %s", self.ticker, json.dumps(more_info, indent=4))

        # Update the cache with new data
        new_more_info = {
            "displayName": "Apple Inc.",
            "sector": "Technology",
            "volume": 1000000,
            "currency": "USD"
        }
        self.cache.put_more_info(self.ticker, new_more_info)

        # Retrieve the updated data
        updated_more_info = self.cache.get_more_info(self.ticker)
        logger.info("Updated more info for %s: %s", self.ticker, json.dumps(updated_more_info, indent=4))

    def test_set_ticker_info(self):
        """
        Test the MyDBCache class for setting
        ticker info data.
        """
        info = {
            "displayName": "Apple Inc.",
            "sector": "Technology",
            "volume": 1000000,
            "currency": "USD",
            "hot": 1
        }

        self.cache.set_ticker_info(self.ticker, info)

    def test_cache_kpi(self):
        """
        Test set_cache_kpi and get_cache_kpi for storing
        and retrieving KPI data.
        """
        name = "momentum"
        last_session = datetime.now()
        value = {"score": 0.85, "signal": "buy"}

        # Store KPI in cache
        self.cache.set_cache_kpi(self.ticker, name, last_session, value)

        # Retrieve KPI from cache
        result = self.cache.get_cache_kpi(self.ticker, name, last_session)
        self.assertIsNotNone(result)
        self.assertEqual(result["score"], 0.85)
        self.assertEqual(result["signal"], "buy")
        self.assertIn("update_ts", result)


if __name__ == "__main__":
    unittest.main()

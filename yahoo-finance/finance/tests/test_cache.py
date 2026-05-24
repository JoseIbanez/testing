

import logging
import json

from finance.yfin.cache import MyDBCache

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_fast_info_cache():
    """
    Test the MyDBCache class for storing
    and retrieving fast_info data.
    """

    cache = MyDBCache()
    ticker = "AAPL"
    fast_info = cache.get_fast_info(ticker)
    logger.info("Fast info for %s: %s", ticker, json.dumps(fast_info, indent=4))

    # Update the cache with new data
    new_fast_info = {
        "currentPrice": 150.0,
        "yearHigh": 200.0,
        "twoHundredDayAverage": 120.0
    }
    cache.put_fast_info(ticker, new_fast_info)

    # Retrieve the updated data
    updated_fast_info = cache.get_fast_info(ticker)
    logger.info("Updated fast info for %s: %s", ticker, json.dumps(updated_fast_info, indent=4))        




def test_more_info_cache():
    """
    Test the MyDBCache class for storing
    and retrieving more_info data.
    """

    cache = MyDBCache()
    ticker = "AAPL"
    more_info = cache.get_more_info(ticker)
    logger.info("More info for %s: %s", ticker, json.dumps(more_info, indent=4))

    # Update the cache with new data
    new_more_info = {
        "displayName": "Apple Inc.",
        "sector": "Technology",
        "volume": 1000000,
        "currency": "USD"
    }
    cache.put_more_info(ticker, new_more_info)

    # Retrieve the updated data
    updated_more_info = cache.get_more_info(ticker)
    logger.info("Updated more info for %s: %s", ticker, json.dumps(updated_more_info, indent=4))


def test_set_ticker_info():
    """
    Test the MyDBCache class for setting
    ticker info data.
    """

    cache = MyDBCache()

    ticker = "AAPL"
    info = {
        "displayName": "Apple Inc.",
        "sector": "Technology",
        "volume": 1000000,
        "currency": "USD",
        "hot": 1    
    }
    


    cache.set_ticker_info(ticker, info)


if __name__ == "__main__":
    test_fast_info_cache()
    test_more_info_cache()
    test_set_ticker_info()

import logging

from matplotlib import ticker
import yfinance as yf
from finance.yfin.cache import MyDBCache


from finance.yfin.cache import MyDBCache
from finance.yfin.inventory import get_ticker_list


logger = logging.getLogger(__name__)




def get_fast_info(ticker:str,force=False):

    # First try to get from cache
    my_cache = MyDBCache()

    if force:
        fast_info = None
    else:
        fast_info = my_cache.get_fast_info(ticker)
        
    if fast_info:
        logger.debug("Cache hit for %s: %s", ticker, fast_info)
        return fast_info

    logger.debug("Cache miss for %s, fetching from Yahoo Finance", ticker)
    # If not in cache, fetch from Yahoo Finance

    try:
        #ticker_obj = tickers.tickers[ticker]
        yf_ticker = yf.Ticker(ticker)
        fast_info = {   
                "lastPrice": float(yf_ticker.fast_info['lastPrice']),
                "yearHigh": float(yf_ticker.fast_info['yearHigh']),
                "twoHundredDayAverage": float(yf_ticker.fast_info['twoHundredDayAverage']),
                "fiftyDayAverage": float(yf_ticker.fast_info['fiftyDayAverage'])
        }


    except (AttributeError, TypeError, KeyError) as e:
        logger.error("Error fetching data for %s: %s", ticker, str(e))
        my_cache.put_error(ticker)
        return None


    # Store in cache for future use
    my_cache.put_fast_info(ticker, fast_info)

    return fast_info


def get_more_info(ticker):

    # First try to get from cache
    my_cache = MyDBCache()
    more_info = my_cache.get_more_info(ticker)
    if more_info:
        logger.debug("Cache hit for %s", ticker)
        return more_info

    logger.debug("Cache miss for %s, fetching from Yahoo Finance", ticker)
    # If not in cache, fetch from Yahoo Finance

    try:
        yf_ticker = yf.Ticker(ticker)
        more_info = yf_ticker.info

    except (AttributeError, TypeError) as e:
        logger.error("Error fetching data for %s: %s", ticker, str(e))
        more_info = {}

    # Store in cache for future use
    my_cache.put_more_info(ticker, more_info)

    return more_info


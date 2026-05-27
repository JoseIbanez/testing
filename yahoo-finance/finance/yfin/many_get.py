import logging

import yfinance as yf
from finance.yfin.cache import MyDBCache
import re
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
my_cache = MyDBCache()


def get_ticker_list(file_name="STOXX_600"):
    """
    Read tickers from a CSV file (tab or comma separated, with header "ticker").
    :param: file_name: Name of the CSV file (without .csv extension) located in ./data/index/
    :return: List of tickers
    """

    tickers_list = []
    index_file = f"./data/index/{file_name}.csv"

    with open(index_file, "r") as f:
        next(f)  # skip header
        for line in f:
            ticker = line.strip().split("\t")[0].split(",")[0]

            if not ticker:
                continue

            # Replace market-specific suffixes with Yahoo Finance format
            #ticker = re.sub(r'\.S$', '.SW', ticker)  # Swiss stocks
            #ticker = re.sub(r'\.CO$', '.VI', ticker)  # Vienna stocks
            tickers_list.append(ticker)


    logger.info("Loaded %d tickers from file", len(tickers_list))
    return tickers_list




def get_fast_info(ticker):

    # First try to get from cache
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
                "twoHundredDayAverage": float(yf_ticker.fast_info['twoHundredDayAverage'])
        }

    except (AttributeError, TypeError, KeyError) as e:
        logger.error("Error fetching data for %s: %s", ticker, str(e))
        return None


    # Store in cache for future use
    my_cache.put_fast_info(ticker, fast_info)

    return fast_info


def get_more_info(ticker):

    # First try to get from cache
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

def get_args():
    parser = argparse.ArgumentParser(description="Fetch and cache stock data from Yahoo Finance")
    parser.add_argument("--index", "-i", type=str, default="", help="Name of the index file (without .csv) in ./data/index/")
    parser.add_argument("--init", action=argparse.BooleanOptionalAction, help="Initialize the DB cache")
    parser.add_argument("--check", "-c", action=argparse.BooleanOptionalAction, help="Check tickers in the DB")
    return parser.parse_args()


def main():


    args = get_args()


    if args.init:
        my_cache.create_table()
        logger.info("Cache initialized")
        return


    if args.index:
        logger.info("Importing tickers from index: %s", args.index)
        import_index(args.index)
        return


    if args.check:
        logger.info("Checking tickers in DB")
        check_ticker_list()
        return



def check_ticker_list():

    tickers_list = my_cache.query_ticker_list()

    for ticker in tickers_list:
        check_ticker(ticker)




def import_index(index):

    tickers_list = get_ticker_list(index)

    for ticker in tickers_list:
        check_ticker(ticker)




def check_ticker(ticker):

        fast_info = get_fast_info(ticker)
        if not fast_info:
            return


        last_price = fast_info['lastPrice']
        year_high = fast_info['yearHigh']
        d200_avg = fast_info['twoHundredDayAverage']

        note = ""
        if last_price > year_high * 0.97:
            note = note + "*"
            if last_price < d200_avg * 1.30:
                note = note + "*"


        print(f"Information for {ticker}:  {last_price:.2f} / {year_high:.2f} / {d200_avg:.2f} {note}")
        if note != "**":
            return


        more_info = get_more_info(ticker)

        allTimeHigh = more_info.get("allTimeHigh", 0)
        if last_price > allTimeHigh * 0.97 and allTimeHigh > 0:
            note = note + "*"

        more_info['hot'] = len(note)
        my_cache.set_ticker_info(ticker, more_info)



        if note == "***":
            print(f"  --> {ticker} {note}")





if __name__ == "__main__":
    main()
from enum import Enum
import logging
import yfinance as yf
import argparse

from finance.yfin.cache import MyDBCache
from finance.yfin.inventory import get_ticker_list
from finance.yfin.fetch_info import get_fast_info, get_more_info


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
my_cache = MyDBCache()

class MyLabels(Enum):
    MAX = "MAX"
    M_YTD = "M_YTD"
    SMA200 = "SMA200"
    SMA5 = "SMA5"
    SMA10 = "SMA10"
    VLTY5 = "VLTY5"
    VLTY30 = "VLTY30"



def check_ticker_list():
    """
    Check all tickers in the DB cache.
    """

    tickers_list = my_cache.query_ticker_list()

    for ticker in tickers_list:
        check_ticker(ticker)


def import_index(index):
    """
    Import tickers from a given index file and store in the DB cache.
    """

    tickers_list = get_ticker_list(index)

    for ticker in tickers_list:
        check_ticker(ticker)


def check_ticker(ticker):
    """
    Check a single ticker
    """    

    fast_info = get_fast_info(ticker)
    if not fast_info:
        return


    last_price = fast_info['lastPrice']
    year_high = fast_info['yearHigh']
    d200_avg = fast_info['twoHundredDayAverage']

    notes = set()

    if last_price > year_high * 0.97:
        notes.add(MyLabels.M_YTD)

    if last_price > d200_avg * 1.05 and last_price < d200_avg * 1.30:
        notes.add(MyLabels.SMA200)


    print(f"Information for {ticker}:  {last_price:.2f} / {year_high:.2f} / {d200_avg:.2f} {[note.value for note in notes]}")

    if len(notes) < 2:
        return


    more_info = get_more_info(ticker)

    allTimeHigh = more_info.get("allTimeHigh", 0)
    if last_price > allTimeHigh * 0.97 and allTimeHigh > 0:
        notes.add(MyLabels.MAX)

    more_info['hot'] = len(notes)
    my_cache.set_ticker_info(ticker, more_info)



    if len(notes) == 3:
        print(f"  --> {ticker} {notes}")



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

if __name__ == "__main__":
    main()
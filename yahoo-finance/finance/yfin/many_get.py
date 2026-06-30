from enum import Enum
import logging
import yfinance as yf
import argparse

from finance.yfin.cache import MyDBCache
from finance.yfin.inventory import get_ticker_list
from finance.yfin.fetch_info import get_fast_info, get_more_info
from finance.yfin.main_kpi import calculate_kpis

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
my_cache = MyDBCache()

class MyLabels(Enum):
    MAX = "MAX"
    MAX_97 = "MAX_97"
    MAX_95 = "MAX_95"
    MAX_90 = "MAX_90"
    M_YTD = "M_YTD"
    M95_YTD = "M95_YTD"
    M90_YTD = "M90_YTD"
    M_W52 = "M_W52"
    SMA200 = "SMA200"
    SMA5 = "SMA5"
    SMA10 = "SMA10"
    SMA50 = "SMA50"
    VLTY5 = "VLTY5"
    VLTY20 = "VLTY20"
    VLTY80 = "VLTY80"
    RETEST = "RETEST"

class Notes:

    def __init__(self):
        self.notes = set()

    def add(self, note: MyLabels):
        self.notes.add(note)

    def discard(self, note: MyLabels):
        self.notes.discard(note)

    def has(self, note: MyLabels):
        return note in self.notes
    
    def __len__(self):
        return len(self.notes)

    def __str__(self):
        return ",".join([note.value for note in self.notes])
    



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
    d50_avg = fast_info['fiftyDayAverage']

    notes = Notes()

    if last_price > year_high * 0.97:
        notes.add(MyLabels.M_YTD)

    elif last_price > year_high * 0.95:
        notes.add(MyLabels.M95_YTD)

    if last_price > d200_avg * 1.05 and last_price < d200_avg * 1.30:
        notes.add(MyLabels.SMA200)

    if last_price > d50_avg and last_price < d50_avg * 1.10 and last_price < d200_avg:
        notes.add(MyLabels.SMA50)


    print(f"Information for {ticker}:  {last_price:.2f} / {year_high:.2f} / {d200_avg:.2f} {notes}")
    if len(notes) < 2:
        return


    notes.discard(MyLabels.M_YTD)

    more_info = get_more_info(ticker)

    all_high = more_info.get("allTimeHigh", 0)
    if all_high <= 0:
        pass

    elif last_price > all_high * 0.99:
        notes.add(MyLabels.MAX)

    elif last_price > all_high * 0.97:
        notes.add(MyLabels.MAX_97)

    elif last_price > all_high * 0.95:
        notes.add(MyLabels.MAX_95)

    elif last_price > all_high * 0.90:
        notes.add(MyLabels.MAX_90)

    more_info['hot'] = len(notes)
    my_cache.set_ticker_info(ticker, more_info)

    if len(notes) < 2:
        return


    kpis = calculate_kpis(ticker)
    if kpis.get("volatility_near_max") < kpis.get("volatility_20d_p90") and kpis.get("volatility_20d_p90") < 3 and kpis.get("volatility_200d_p99") < 10:
        notes.add(MyLabels.VLTY5)

    if kpis.get("volatility_20d_p90") < 3:
        notes.add(MyLabels.VLTY20)

    if "MAX_FALL" in kpis.get("labels", []):
        notes.add(MyLabels.RETEST)

    if len(notes) >= 2:
        name = more_info.get("shortName", "")
        print(f"  --> {ticker}, {name}: {notes}")



def get_args():
    parser = argparse.ArgumentParser(description="Fetch and cache stock data from Yahoo Finance")
    parser.add_argument("--index", "-i", type=str, default="", help="Name of the index file (without .csv) in ./data/index/")
    parser.add_argument("--init", action=argparse.BooleanOptionalAction, help="Initialize the DB cache")
    parser.add_argument("--check", "-c", action=argparse.BooleanOptionalAction, help="Check tickers in the DB")
    parser.add_argument("--ticker", "-t", type=str, default=None, help="Ticker symbol to check")
    return parser.parse_args()


def main():

    args = get_args()

    if args.init:
        my_cache.create_table()
        logger.info("Cache initialized")
        return

    if args.ticker:
        logger.info("Checking ticker: %s", args.ticker)
        check_ticker(args.ticker)
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
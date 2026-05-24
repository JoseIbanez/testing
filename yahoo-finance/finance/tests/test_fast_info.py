import logging
import json
import yfinance as yf

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ticker = "MRK.DE"

tickers = yf.Tickers([ticker])
ticker_obj = tickers.tickers[ticker]
fast_info = {
        "lastPrice": tickers.tickers[ticker].fast_info['lastPrice'],
        "yearHigh": tickers.tickers[ticker].fast_info['yearHigh'],
        "twoHundredDayAverage": tickers.tickers[ticker].fast_info['twoHundredDayAverage'],
        "exchange": tickers.tickers[ticker].fast_info['exchange']
}

# Fast info
logger.info("Fast info for %s: %s", ticker, fast_info)
logger.info("Fast info for %s: %s", ticker, ticker_obj.fast_info)

# Info

more_info = ticker_obj.info
my_info = {
    "displayName": more_info.get("displayName") or more_info.get("longName"),
    "sector": more_info.get("sector"),
    "industry": more_info.get("industry"),
    "exchange": more_info.get("exchange"),
    "fiftyTwoWeekHigh": more_info.get("fiftyTwoWeekHigh"),
    "allTimeHigh": more_info.get("allTimeHigh"),
    "volume": more_info.get("volume"),
    "currency": more_info.get("currency"),
}



logger.info("Info for %s: %s", ticker, ticker_obj.info)
logger.info("My info for %s: %s", ticker, json.dumps(my_info,indent=2))
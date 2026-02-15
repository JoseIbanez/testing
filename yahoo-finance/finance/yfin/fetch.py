import os
import yfinance as yf
import time
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def yahoo_fetch(ticker: str, period: str = "3mo", interval: str = "1d"):
    """
    Fetches historical stock data from Yahoo Finance.
    -  Check if data exists in the data folder
    -  If not, fetch from Yahoo Finance
    -  Save the data to the data folder

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        period (str): The period to fetch data for (e.g., "3mo", "1y", "max").
        interval (str): The interval between data points (e.g., "1d", "1wk", "1mo").
    """

    # Check if cache file exists and is less than 1 day old
    cache_file = f"./data/{ticker}_{period}.csv"

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < 86400:
        df = pd.read_csv(cache_file)
        logger.info("Using cached data for %s (%s), rows:%d", ticker, period, len(df))
        return df


    # Download data from Yahoo Finance
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    logger.info("Downloaded data for %s (%s)", ticker, period)


    # Save the data to the data folder
    df.to_csv(cache_file)
    logger.info("Saved data for %s (%s) to %s", ticker, period, cache_file)
    return df   



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    yahoo_fetch("AAPL", period="6mo")
    yahoo_fetch("DBK.DE", period="6mo")
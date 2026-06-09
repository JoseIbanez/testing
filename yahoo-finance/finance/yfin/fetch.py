import os
import yfinance as yf
import time
import pandas as pd
import logging
from datetime import datetime, timedelta

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

    if "ytd" in period:
        period_suffix = datetime.strftime(datetime.now(), "%Y")
        period_cache = 30 * 24 * 3600
    elif "y" in period or "max" in period:
        period_suffix = datetime.strftime(datetime.now() - timedelta(days=365), "%Y")
        period_cache = 7 * 24 * 3600
    elif "mo" in period:
        period_suffix = datetime.strftime(datetime.now(), "%Y-%m")
        period_cache = 24 * 3600
    else:
        period_suffix = ""
        period_cache = 24 * 3600



    # Check if cache file exists and is less than 1 day old
    cache_file = f"./data/{ticker}_{period}_{period_suffix}.csv"

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < period_cache:
        df = pd.read_csv(cache_file)
        # Normalize to midnight next day to align with Yahoo Finance's convention
        df['Date'] = pd.to_datetime(df['Date'],utc=True).dt.normalize() + pd.Timedelta(days=1) 
        logger.debug("Dataframe: \n%s", df.dtypes)
        df.set_index('Date', inplace=True) 

        # Remove empty rows
        df = df[df['Close'].notna()]

        logger.debug("Using cached data for %s (%s), rows:%d", ticker, period, len(df))
        return df


    # Download data from Yahoo Finance
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    logger.info("Downloaded data for %s (%s)", ticker, period)


    # Save the data to the data folder
    df = df[df['Close'].notna()]
    df.to_csv(cache_file)
    logger.info("Saved data for %s (%s) to %s", ticker, period, cache_file)
    return df   


def load_ticker(ticker: str):

    df_max = yahoo_fetch(ticker, period="max")
    df_ytd = yahoo_fetch(ticker, period="ytd")
    df_1mo = yahoo_fetch(ticker, period="1mo")
    full_df = pd.concat([df_max, df_ytd, df_1mo])
    full_df = full_df[~full_df.index.duplicated(keep='last')]

    full_df.to_csv(f"./data/{ticker}_full.csv")
    return full_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    yahoo_fetch("AAPL", period="max")
    yahoo_fetch("AAPL", period="ytd")
    yahoo_fetch("AAPL", period="1mo")


    yahoo_fetch("DBK.DE", period="max")
    yahoo_fetch("DBK.DE", period="ytd")
    yahoo_fetch("DBK.DE", period="1mo")


    yahoo_fetch("IBE.MC", period="max")
    yahoo_fetch("IBE.MC", period="ytd")
    yahoo_fetch("IBE.MC", period="1mo")

    load_ticker("MU")
    load_ticker("XOM")    
import os
import yfinance as yf
import time
import pandas as pd
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

def load_serie(ticker: str):
    """
    Download last historical data for a ticker and save to a CSV
    This function does an incremental download:
    - Load current data from CSV if exists
    - Extract last date from CSV
    - Download new data from Yahoo Finance starting from the last date
    - Save the new data to the CSV, appending to existing data
    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
    Returns:
        df (pd.DataFrame): The combined DataFrame containing existing and new data.
    """

    # Determine last date from existing CSV
    cache_folder = get_prefix(ticker)
    cache_file = f"{cache_folder}{ticker}_full.csv"

    if os.path.exists(cache_file):
        df_existing = pd.read_csv(cache_file, index_col='Date', parse_dates=True)
        #df_existing.index = df_existing.index.tz_localize('UTC')
        #print("df_existing")
        #print(df_existing.tail())

        last_date = df_existing.index.max()
        logger.info("Ticker:%s, Existing data found, last date: %s", ticker, last_date)
    else:
        df_existing = pd.DataFrame()
        last_date = None
        logger.info("Ticker:%s, No existing data found.", ticker)


    if last_date and last_date >= datetime.today().replace(tzinfo=timezone.utc) - timedelta(days=1):
        logger.info("Ticker:%s, Data is already up to date (last date: %s)", ticker, last_date)
        return df_existing

    # Download new data from Yahoo Finance
    stock = yf.Ticker(ticker)
    
    if last_date:
        start_date = (last_date - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        logger.info("Ticker:%s, Downloading new data starting from %s", ticker, start_date)
        df_new = stock.history(start=start_date, interval="1d")
        df_new.index = df_new.index.tz_localize(None).tz_localize('UTC')

        #df_new['Date'] = pd.to_datetime(df_new.index, utc=True).tz_convert('UTC')
        #increase one day if hour is big than 12
        #df_new['Date'] = df_new['Date'].apply(lambda x: x + pd.Timedelta(days=1) if x.hour >= 12 else x)
        #print(df_new.head())
        #df_new['Date'] = df_new['Date'].dt.normalize()
        #df_new.set_index('Date', inplace=True)
        #print(df_new.head())    

    else:
        logger.info("Ticker:%s, Downloading full history", ticker)
        df_new = stock.history(period="max", interval="1d")


    # Combine existing and new data, and save to CSV
    if not df_new.empty:
        df_combined = pd.concat([df_existing, df_new])
        df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
        df_combined.to_csv(cache_file)
        logger.info("Saved updated data for %s to %s", ticker, cache_file)
    else:
        logger.info("No new data available for %s", ticker)

    return df_combined


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
    cache_folder = get_prefix(ticker)
    cache_file = f"{cache_folder}{ticker}_{period}_{period_suffix}.csv"

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
    df.index = pd.to_datetime(df.index, utc=True).normalize() + pd.Timedelta(days=1) 


    # Save the data to the data folder
    df = df[df['Close'].notna()]
    df.to_csv(cache_file)
    logger.info("Saved data for %s (%s) to %s", ticker, period, cache_file)
    return df   


def get_prefix(ticker: str):
    """
    Returns the prefix for the cache file based on the ticker symbol.
    Create folder if it does not exist.
    """

    if "." in ticker:
        market = ticker.split(".")[1]
    else:
        market = "_" + ticker[1]

    folder = f"./data/series/{market}/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder



def load_ticker(ticker: str):

    df_max = yahoo_fetch(ticker, period="max")
    df_ytd = yahoo_fetch(ticker, period="ytd")
    df_1mo = yahoo_fetch(ticker, period="1mo")
    full_df = pd.concat([df_max, df_ytd, df_1mo])
    full_df = full_df[~full_df.index.duplicated(keep='last')]

    cache_folder = get_prefix(ticker)
    full_df.to_csv(f"{cache_folder}{ticker}_full.csv")
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
import os
import yfinance as yf
import time
import pandas as pd
import logging
from datetime import datetime, timezone

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
        df_existing = df_existing[df_existing['Close'].notna()] # Remove empty rows
        last_date = df_existing.index.max()
        logger.debug("Ticker:%s, Existing data found, last date: %s", ticker, last_date)
    else:
        df_existing = pd.DataFrame()
        last_date = None
        logger.debug("Ticker:%s, No existing data found.", ticker)

    # Check if cache file is fresh, main use when market is closed
    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file)) < 4 * 3600:
        logger.debug("Ticker:%s, Cache file is fresh (last modified: %s), using existing data.", ticker, time.ctime(os.path.getmtime(cache_file)))
        return df_existing

    # We are updated
    if last_date and last_date >= datetime.today().replace(tzinfo=timezone.utc):
        logger.debug("Ticker:%s, Data is already up to date (last date: %s)", ticker, last_date)
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
        df_new.index = df_new.index.tz_localize(None).tz_localize('UTC')


    # Combine existing and new data, and save to CSV
    if not df_new.empty:
        df_combined = pd.concat([df_existing, df_new])
        df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
        df_combined = df_combined[df_combined['Close'].notna()] # Remove empty rows
        df_combined.to_csv(cache_file)
        logger.debug("Saved updated data for %s to %s", ticker, cache_file)
    else:
        logger.info("No new data available for %s", ticker)

    return df_combined



def get_prefix(ticker: str):
    """
    Returns the prefix for the cache file based on the ticker symbol.
    Create folder if it does not exist.
    """

    if "." in ticker:
        market = ticker.split(".")[1]
    else:
        market = "_" + ticker[0]

    folder = f"./data/series/{market}/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder




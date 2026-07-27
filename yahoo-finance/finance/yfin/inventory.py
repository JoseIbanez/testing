
import pandas as pd
import yfinance as yf
import logging


INDEX_SUFIX_PER_COUNTRY = {
    "Denmark": ".CO",
    "Finland": ".HE",
    "France": ".PA",
    "Germany": ".DE",
    "Italy": ".MI",
    "Netherlands": ".AS",
    "Spain": ".MC",
    "Sweden": ".ST",
    "Switzerland": ".SW",
    "United Kingdom": ".L",
    }

logger = logging.getLogger(__name__)


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




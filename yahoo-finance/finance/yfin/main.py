import logging
import pandas as pd
import json
import argparse

from finance.yfin.fetch import load_ticker
from finance.yfin.kpi import add_indicators, kmeans_clustering, get_support_resistance, get_swing_points, get_summary_kpi, get_last_volatility

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and analyze stock data")
    parser.add_argument("--ticker", type=str, default="AAPL", help="Ticker symbol to analyze")
    return parser.parse_args()


def main():
    args = parse_args()
    ticker = args.ticker

    #ticker = "DBK.DE"
    #ticker = "DTE.DE"
    #ticker = "XOM"
    #ticker = "DOW"
    #ticker = "BAS.DE"
    #ticker = "STB.OL"
    calculate_kpis(ticker)


def calculate_kpis(ticker):

    df = load_ticker(ticker)
    df = add_indicators(ticker, df)
    kmeans_levels = kmeans_clustering(ticker, df)
    levels = get_support_resistance(ticker, df)
    swing_points = get_swing_points(ticker, df)

    summary = get_summary_kpi(ticker, df)

    logger.info("Dataframe: \n%s", df.tail())
    #logger.info("Kmeans Levels: \n%s", kmeans_levels)
    logger.info("Summary: \n%s", json.dumps(levels, indent=4))
    #logger.info("Swing Points: \n%s", swing_points)
    logger.info("Summary: \n%s", json.dumps(summary, indent=4))


    last_volatility = get_last_volatility(ticker, df)
    logger.info("Last volatility: \n%s", json.dumps(last_volatility, indent=4))


if __name__ == "__main__":
    main()

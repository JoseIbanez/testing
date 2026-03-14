import logging
import pandas as pd


from finance.yfin.fetch import yahoo_fetch
from finance.yfin.kpi import add_indicators, kmeans_clustering, get_support_resistance, get_swing_points

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    period = "2y"

    ticker = "DBK.DE"

    #ticker = "DTE.DE"


    df = yahoo_fetch(ticker, period)
    df = add_indicators(ticker, df)
    kmeans_levels = kmeans_clustering(ticker, df)
    levels = get_support_resistance(ticker, df)
    swing_points = get_swing_points(ticker, df)

    logger.info("Dataframe: \n%s", df.tail())
    logger.info("Kmeans Levels: \n%s", kmeans_levels)
    logger.info("Support/Resistance Levels: \n%s", levels)
    logger.info("Swing Points: \n%s", swing_points)


if __name__ == "__main__":
    main()

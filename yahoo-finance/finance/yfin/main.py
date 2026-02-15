import logging
import pandas as pd


from finance.yfin.fetch import yahoo_fetch
from finance.yfin.kpi import add_indicators

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    ticker = "DBK.DE"
    period = "6mo"
    df = yahoo_fetch(ticker, period)
    df = add_indicators(ticker, df)
    logger.info("Dataframe: \n%s", df)


if __name__ == "__main__":
    main()

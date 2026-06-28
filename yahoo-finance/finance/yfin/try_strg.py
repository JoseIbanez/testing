
import logging
import pandas as pd
import json
import argparse
from datetime import datetime, timezone
from finance.yfin.fetch_serie import load_serie
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ShareLot:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.shares = 0
        self.pl = 0.0

        self.buy_price = None
        self.buy_date = None
        self.sell_price = None
        self.sell_date = None


    def buy(self, shares: float, price: float, date: datetime):
        self.shares += shares
        self.buy_price = price
        self.buy_date = date
        logger.info("%s, %s +%d at price:%.02f", date, self.ticker, shares, price)


    def close(self, price: float, date: datetime):
        self.sell_price = price
        self.sell_date = date

        if self.shares > 0:
            pl = (self.sell_price - self.buy_price) * self.shares
            self.pl += pl
            logger.info("%s, %s -%d at price:%.2f // PL:%.02f, ACCU:%.02f", date, self.ticker, self.shares, price, pl, self.pl)

        self.shares = 0
        self.buy_price = None
        self.buy_date = None
        self.sell_price = None
        self.sell_date = None



def get_serie_up_to_date(ticker: str, cur_date: datetime, full_df: pd.DataFrame):

    df = full_df[full_df.index <= cur_date]

    if df.empty:
        logger.info("Ticker %s, no data available on %s", ticker, cur_date)
        return pd.DataFrame()  # Return an empty DataFrame

    if df.index[-1] < cur_date:
        logger.debug("Ticker %s, market was closed on %s", ticker, cur_date)
        return pd.DataFrame()  # Return an empty DataFrame

    return df




def apply_dummy_strategy(ticker: str, lot: ShareLot, cur_date: datetime, full_df: pd.DataFrame):

    df = get_serie_up_to_date(ticker, cur_date, full_df)
    if df.empty:
        return


    # if day of week is Monday, buy 10 shares
    if cur_date.weekday() == 0 and lot.shares == 0:
        price = df['Close'].iloc[-1]
        lot.buy(10, price, cur_date)

    # if day of week is Friday, close position
    if cur_date.weekday() == 4 and lot.shares > 0:
        price = df['Close'].iloc[-1]
        lot.close(price, cur_date)


def apply_sma_strategy(ticker: str, lot: ShareLot, cur_date: datetime, full_df: pd.DataFrame):

    df = get_serie_up_to_date(ticker, cur_date, full_df)
    if df.empty:
        return


    sma_5  = df['Close'].rolling(window= 5).mean().iloc[-1]
    sma_10 = df['Close'].rolling(window=10).mean().iloc[-1]
    sma_200 = df['Close'].rolling(window=200).mean().iloc[-1]
    last_price = df['Close'].iloc[-1]


    # Volatility (True Range)
    prev_close = df['Close'].shift(1).fillna(df['Close'])
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - prev_close).abs()
    tr3 = (df['Low'] - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['Volatility'] = true_range / prev_close * 100

    df_200d = df[-200:]
    volatility_200d_max = df_200d['Volatility'].max()
    volatility_200d_p99 = df_200d['Volatility'].quantile(0.99)
    volatility_200d_p98 = df_200d['Volatility'].quantile(0.98)

    if volatility_200d_max > 20 or volatility_200d_p99 > 15 or volatility_200d_p98 > 10:
        logger.info("%s, %s: High volatility detected, skipping strategy. Volatility 200d max: %.2f, p99: %.2f, p98: %.2f", cur_date, ticker, volatility_200d_max, volatility_200d_p99, volatility_200d_p98)
        return


    # if sma_5 > sma_10, buy
    if lot.shares == 0 and sma_5 * .99 > sma_10:
        logger.info("%s, %s: SMA5: %.2f, SMA10: %.2f", cur_date, ticker, sma_5, sma_10)
        price = last_price
        to_buy = round(1000 / price)
        lot.buy(to_buy, price, cur_date)


    # if sma_5 < sma_10, close position
    if lot.shares > 0 and sma_5 < sma_10:
        logger.info("%s, %s: SMA5: %.2f, SMA10: %.2f", cur_date, ticker, sma_5, sma_10)
        price = df['Close'].iloc[-1]
        lot.close(price, cur_date)


    loss = (-last_price + lot.buy_price) / lot.buy_price * 100 if lot.buy_price else 0
    if loss > 2:
        logger.info("%s, %s: Loss: %.2f", cur_date, ticker, loss)
        price = last_price
        lot.close(price, cur_date)






def main():
    

    ticker =  "AIR.PA"
    lot = ShareLot(ticker=ticker)

    cur_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    full_df = load_serie(ticker)

    while cur_date < datetime.now(tz=timezone.utc):
        cur_date += pd.Timedelta(days=1)

        #apply_dummy_strategy(ticker, lot, cur_date, full_df)
        apply_sma_strategy(ticker, lot, cur_date, full_df)

    last_price = full_df['Close'].iloc[-1]
    lot.close(last_price, cur_date)





if __name__ == "__main__":
    main()

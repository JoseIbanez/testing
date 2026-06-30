
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

        self.stop_loss = None
        self.buy_price = None
        self.buy_date = None
        self.sell_price = None
        self.sell_date = None

    def check_stop_loss(self, price_open: float, price_low:float, date: datetime):

        if self.shares == 0 or self.stop_loss is None:
            return
        
        if price_open <= self.stop_loss:
            self.close(price_open, date, reason="Stop Loss (Open)")
            return
        
        if price_low <= self.stop_loss:
            self.close(self.stop_loss, date, reason="Stop Loss (Low)")
            return

    def update_stop_loss(self, new_stop_loss: float):
        if self.shares == 0:
            return
        
        logger.info("%s, %s: Updating stop loss from %.2f to %.2f", datetime.now(), self.ticker, self.stop_loss, new_stop_loss)
        self.stop_loss = new_stop_loss


    def buy(self, shares: float, price: float, date: datetime, stop_loss: float = None):
        self.shares += shares
        self.buy_price = price
        self.buy_date = date
        self.stop_loss = stop_loss
        logger.info("%s, %s +%d at price:%.02f, SL: %.02f", date, self.ticker, shares, price, stop_loss)


    def close(self, price: float, date: datetime, reason: str = "Close"):
        self.sell_price = price
        self.sell_date = date

        if self.shares > 0:
            pl = (self.sell_price - self.buy_price) * self.shares
            self.pl += pl
            logger.info("%s, %s -%d at price:%.02f // PL:%.02f, ACCU:%.02f, Reason: %s", date, self.ticker, self.shares, price, pl, self.pl, reason)

        self.shares = 0
        self.buy_price = None
        self.buy_date = None
        self.sell_price = None
        self.sell_date = None
        self.stop_loss = None



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


    sma_5  = df['Close'].rolling(window= 5).mean()
    sma_10 = df['Close'].rolling(window=10).mean()
    sma_200 = df['Close'].rolling(window=200).mean()
    ema_200 = df['Close'].ewm(span=200, adjust=False).mean()


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
    volatility_20_max   = df_200d[-20:]['Volatility'].max()


    lot.check_stop_loss(df['Open'].iloc[-1], df['Low'].iloc[-1], cur_date)



    if (volatility_200d_p99 > 5) and lot.shares == 0:
        logger.info("%s, %s: High volatility detected, skipping strategy. Volatility 200d max: %.2f, p99: %.2f, p98: %.2f", cur_date, ticker, volatility_200d_max, volatility_200d_p99, volatility_200d_p98)
        return

    min_price_3d = df['Close'].iloc[-3:].min()
    if (min_price_3d < ema_200.iloc[-1]) and lot.shares == 0:
        logger.info("%s, %s: Price below EMA200, skipping strategy. Last price: %.2f, EMA200: %.2f", cur_date, ticker, min_price_3d, ema_200.iloc[-1])
        return




    # if sma_5 > sma_10, 
   
    if lot.shares == 0 and sma_5.iloc[-1] * .99 > sma_10.iloc[-1]:
        logger.info("%s, %s: SMA5: %.2f, SMA10: %.2f", cur_date, ticker, sma_5.iloc[-1], sma_10.iloc[-1])
        price = last_price
        stop_loss = price - 2 * volatility_20_max / 100 * price  # Stop loss at 2 times the 20-day volatility below the buy price

        to_buy = round(1000 / price)
        lot.buy(to_buy, price, cur_date, stop_loss=stop_loss)


    # if sma_5 < sma_10, close position
    if lot.shares > 0 and sma_5.iloc[-1] < sma_10.iloc[-1]:
        logger.info("%s, %s: SMA5: %.2f, SMA10: %.2f", cur_date, ticker, sma_5.iloc[-1], sma_10.iloc[-1])
        price = df['Close'].iloc[-1]
        lot.close(price, cur_date)


    loss = (-last_price + lot.buy_price) / lot.buy_price * 100 if lot.buy_price else 0
    if loss > 2:
        logger.info("%s, %s: Loss: %.2f", cur_date, ticker, loss)
        price = last_price
        lot.close(price, cur_date)






def main():
    

    ticker = "ALV.DE"
    #ticker = "CS.PA"
    #ticker = "FGR.PA"
    #ticker = "AAPL"
    #ticker = "CIE.MC"
    ticker = "PST.MI"

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

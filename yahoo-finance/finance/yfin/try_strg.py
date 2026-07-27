
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
        self.cost =0.0
        self.pl = 0.0

        self.buy_limit = None
        self.sell_limit = None
        self.stop_loss = None

    def check_stop_loss(self, price_open: float, price_low:float, cur_date: datetime):

        if self.shares == 0 or self.stop_loss is None:
            return
        
        if price_open <= self.stop_loss:
            self.close(price_open, cur_date, reason="Stop Loss (Open)")
            return
        
        if price_low <= self.stop_loss:
            self.close(self.stop_loss, cur_date, reason="Stop Loss (Low)")
            return

    def check_buy_limit(self, price_open: float, price_low:float, cur_date: datetime):

        if self.buy_limit is None:
            return        
        
        if self.shares > 0:
            return
        
        if price_open <= self.buy_limit:
            self.shares += self.shares
            self.buy_price = price_open
            self.buy_date = cur_date
            logger.info("%s, %s +%d at price:%.02f, SL: %.02f", cur_date, self.ticker, self.shares, price_open)





        self.buy_limit = price
        logger.info("%s, %s: Setting buy limit at %.2f", cur_date, self.ticker, price)



    def update_stop_loss(self, new_stop_loss: float, cur_date: datetime):
        if self.shares == 0:
            return
        
        logger.info("%s, %s: Updating stop loss from %.2f to %.2f", cur_date, self.ticker, self.stop_loss, new_stop_loss)
        self.stop_loss = new_stop_loss


    def buy(self, shares: float, price: float, cur_date: datetime, stop_loss: float = None):
        self.shares += shares
        self.cost += shares * price
        self.stop_loss = stop_loss
        logger.info("%s, %s +%d at price:%.02f, SL: %.02f", cur_date, self.ticker, shares, price, stop_loss)


    def close(self, price: float, cur_date: datetime, reason: str = "Close"):

        if self.shares > 0:
            pl = (price * self.shares) - self.cost
            self.pl += pl
            logger.info("%s, %s -%d at price:%.02f // PL:%.02f, ACCU:%.02f, Reason: %s", cur_date, self.ticker, self.shares, price, pl, self.pl, reason)

        self.shares = 0
        self.cost = 0.0
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



def apply_dennis_strategy(ticker: str, lot: ShareLot, cur_date: datetime, full_df: pd.DataFrame):
    """ 
    Dennis strategy: 
    Buy when price is above 20-day high, 
    sell when price is below 10-day low. 
    """

    df = get_serie_up_to_date(ticker, cur_date, full_df)
    if df.empty:
        return

    price_20d_max = df['Close'].iloc[-20:].max()
    price_10d_min = df['Close'].iloc[-10:].min()
    price_last = df['Close'].iloc[-1]

    #The 20-day exponential moving average of the True Range (now widely known as the Average True Range (ATR)).
    atr_20d = df['tr'].ewm(span=20, adjust=False).mean().iloc[-1]
    atr_5d  = df['tr'].ewm(span=5, adjust=False).mean().iloc[-1]

    lot.check_stop_loss(df['Open'].iloc[-1], df['Low'].iloc[-1], cur_date)

    #logger.info("%s, %s: Price: %.2f, MAX20: %.2f, MIN10: %.2f, ATR20: %.2f, ATR5: %.2f", cur_date, ticker, price_last, price_20d_max, price_10d_min, atr_20d, atr_5d)

    if lot.shares == 0 and  price_last >= price_20d_max and atr_20d >= atr_5d:
        logger.info("%s, %s: Price: %.2f, MAX20: %.2f", cur_date, ticker, price_last, price_20d_max)
        price_buy = price_last

        # Stop loss at the higher of the 10-day low or 2 times the 20-day ATR below the buy price
        stop_loss = max(price_10d_min, price_buy - 2 * atr_20d)  


        to_buy = round(10 / atr_20d )
        logger.info("%s, %s: Buying %d shares at %.2f, ATR: %.2f", cur_date, ticker, to_buy, price_buy, atr_20d)


        lot.buy(to_buy, price_buy, cur_date, stop_loss=stop_loss)


    if lot.shares > 0 and price_last > (lot.cost / lot.shares) + atr_20d / 2 and lot.cost < 1200 and atr_20d >= atr_5d:

        logger.info("%s, %s: Price: %.2f, Bought at: %.2f, Cost: %.2f, Shares: %d", cur_date, ticker, price_last, lot.cost / lot.shares, lot.cost, lot.shares)

        price_buy = price_last
        stop_loss = max(price_10d_min, price_buy - 2 * atr_20d)  

        to_buy = round(10 / atr_20d )
        logger.info("%s, %s: Buying %d shares at %.2f, ATR: %.2f", cur_date, ticker, to_buy, price_buy, atr_20d)


        lot.buy(to_buy, price_buy, cur_date, stop_loss=stop_loss)





    if lot.shares > 0:
        stop_loss = max(price_10d_min, price_last - 2 * atr_20d)  
        if stop_loss > lot.stop_loss:
            lot.update_stop_loss(stop_loss, cur_date)


def main():
    

    #ticker = "ALV.DE"
    #ticker = "CS.PA"
    #ticker = "FGR.PA"
    #ticker = "AAPL"
    #ticker = "CIE.MC"
    #ticker = "PST.MI"
    ticker = "SCYR.MC"
    #ticker = "WSM"
    #ticker = "NN.AS"
    ticker = "INGA.AS"

    lot = ShareLot(ticker=ticker)

    cur_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    full_df = load_serie(ticker)

    prev_close = full_df['Close'].shift(1).fillna(full_df['Close'])
    tr1 = full_df['High'] - full_df['Low']
    tr2 = (full_df['High'] - prev_close).abs()
    tr3 = (full_df['Low'] - prev_close).abs()
    full_df['tr'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)


    while cur_date < datetime.now(tz=timezone.utc):
        cur_date += pd.Timedelta(days=1)

        #apply_dummy_strategy(ticker, lot, cur_date, full_df)
        #apply_sma_strategy(ticker, lot, cur_date, full_df)
        apply_dennis_strategy(ticker, lot, cur_date, full_df)

    last_price = full_df['Close'].iloc[-1]
    lot.close(last_price, cur_date)





if __name__ == "__main__":
    main()

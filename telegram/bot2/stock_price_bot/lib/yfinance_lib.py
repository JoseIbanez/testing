import yfinance as yf
from datetime import datetime
import pytz
import logging
import time
import os
from requests import Session
from requests.exceptions import HTTPError
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from stock_price_bot.lib.common import configure_loger
from stock_price_bot.lib.model import Symbol

DATA_PATH =  os.environ.get("DATA_PATH", "/home/ubuntu/Projects/testing/telegram/bot2/sample-data")

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

logger = logging.getLogger(__name__)

sessionXL = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket),
    backend=SQLiteCache(f"{DATA_PATH}/yfinanceXL.cache"),
    expire_after = 3600,
)

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket),
    backend=SQLiteCache(f"{DATA_PATH}/yfinance.cache"),
    expire_after = 60,
)

valList=['ITX.MC', 'ELE.MC', 'EOAN.DE', 'VOW3.DE', 'DTE.DE', 'DBK.DE', 'BAYN.DE', 'ALV.DE', 'LHA.DE', 'CS.PA', 'VOD.L', 'NVDA', 'MSF.DE' ]



def get_symbol_info(symbol_id:str) -> Symbol:

    try:

        logger.info("Geting infor for %s",symbol_id)

        time0 = time.time()
        tickerXL=yf.Ticker(symbol_id,session=sessionXL)

        if tickerXL.info is None:
            logger.error("Symbol:%s not found",symbol_id)
            return None

        s = Symbol()
        s.id = symbol_id
        s.displayName = tickerXL.info.get('displaytName') or tickerXL.info.get('shortName') 
        s.marketState = tickerXL.info.get('marketState')
        s.currency = tickerXL.info.get('currency')
        exchangeTimezoneName = tickerXL.info.get('exchangeTimezoneName')

        s.previousClose = tickerXL.fast_info.get('previousClose')
        s.lastPrice = tickerXL.fast_info.get('lastPrice')

        ticker = None
        opening = check_opening(symbol_id,exchangeTimezoneName)

        if s.marketState == "REGULAR" or opening:
            ticker=yf.Ticker(symbol_id,session=session)
            s.lastPrice = ticker.fast_info.get('lastPrice')
        
        if opening and ticker:
            s.marketState = ticker.info.get('marketState')
            s.previousClose = ticker.fast_info.get('previousClose')


        s.priceVariation = (s.lastPrice - s.previousClose)/s.previousClose*100

        logger.info("Symbol:%s updated, delay:%.2fsec",symbol_id,time.time()-time0)

    except HTTPError as e:
        logger.error(e)
        logger.error("Waiting for rate limit")
        time.sleep(60)
        return None

    except AttributeError:
        logger.error("Symbol:%s not found",symbol_id)
        return None



    return s

def check_opening(symbol_id,symbol_tz):

    opening = False
    try:
        tz=pytz.timezone(symbol_tz)
        now = datetime.now(tz)
        current_hour = now.strftime("%H")
    except pytz.UnknownTimeZoneError:
        return False


    if current_hour in "09,10":
        logger.info("Symbol:%s local hour:%s Opening hours", symbol_id,now )
        opening = True


    return opening


def main():

    configure_loger()


    for val in valList:

        text = get_symbol_info(val)
        print(text)




if __name__ == "__main__":
    main()

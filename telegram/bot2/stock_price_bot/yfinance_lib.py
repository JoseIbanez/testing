import yfinance as yf
import requests_cache
import logging
import time
import os
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from stock_price_bot.common import configure_loger

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



def get_symbol_info(symbol_id):

    logger.info("Geting infor for %s",symbol_id)

    time0 = time.time()
    tickerXL=yf.Ticker(symbol_id,session=sessionXL)

    if not tickerXL.info:
        logger.error("Symbol:%s not found",symbol_id)
        return None

    name = tickerXL.info.get('displaytName') or tickerXL.info.get('shortName') 
    marketState = tickerXL.info.get('marketState')
    currency = tickerXL.info.get('currency')

    previousClose = tickerXL.fast_info.get('previousClose')
    lastPrice = tickerXL.fast_info.get('lastPrice')

    if marketState == "OPENED":
        marketState = ""
        ticker=yf.Ticker(symbol_id,session=session)
        lastPrice = ticker.fast_info.get('lastPrice')
    
    var = (lastPrice - previousClose)/previousClose*100


    result = f"{symbol_id} {name}:\n  LastPrice:{lastPrice:.3f} {currency} {var:+.2f}% {marketState}" 

    
    logger.info("Symbol:%s updated, delay:%.2fsec",symbol_id,time.time()-time0)

    return result


def main():

    configure_loger()


    for val in valList:

        text = get_symbol_info(val)
        print(text)




if __name__ == "__main__":
    main()

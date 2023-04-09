import yfinance as yf
import requests_cache
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

sessionXL = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket),
    backend=SQLiteCache("yfinanceXL.cache"),
    expire_after = 3600,
)

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket),
    backend=SQLiteCache("yfinance.cache"),
    expire_after = 60,
)


valList=['ITX.MC', 'ELE.MC', 'EOAN.DE', 'VOW3.DE', 'DTE.DE', 'DBK.DE', 'BAYN.DE', 'ALV.DE', 'LHA.DE', 'CS.PA', 'VOD.L', 'NVDA', 'MSF.DE' ]


tickers=yf.Tickers(' '.join(valList),session=session)
tickersXL=yf.Tickers(' '.join(valList),session=sessionXL)

for val in valList:

    name = tickersXL.tickers[val].info.get('displaytName') or tickersXL.tickers[val].info.get('shortName') 
    marketState = tickersXL.tickers[val].info.get('marketState')
    previousClose = tickersXL.tickers[val].fast_info.get('previousClose')

    lastPrice = tickers.tickers[val].fast_info.get('lastPrice')
    var = (lastPrice - previousClose)/previousClose*100

    if marketState == "OPENED":
        marketState = ""

    print(f"{val} {name}: PreviousClose:{previousClose:.3f} LastPrice:{lastPrice:.3f} {var:+.2f}% {marketState}" )
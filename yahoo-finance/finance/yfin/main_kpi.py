import logging
import pandas as pd
import json
import argparse
from datetime import datetime

from finance.yfin.fetch_serie import load_serie
from finance.yfin.kpi import add_indicators, get_last_volatility, get_lateral_rectangle, detect_break_retest, adjust_dividents
from finance.yfin.cache import MyDBCache

logger = logging.getLogger(__name__)
my_cache = MyDBCache()

def calculate_kpis(ticker,force=False):

    df = load_serie(ticker)
 
    if len(df) == 0:
        return None
    
    last_session:datetime = df.index[-1].to_pydatetime()  

    force = True
    if not force:
        cache_field = my_cache.get_cache_kpi(ticker, "kpi_basic", last_session, ttl= 4 * 24 * 3600)
        if cache_field is not None:
           return cache_field


    df = adjust_dividents(ticker, df)
    df = add_indicators(ticker, df)

    kpis = get_last_volatility(ticker, df)
    retest = detect_break_retest(ticker, df)


    my_cache.set_cache_kpi(ticker, "kpi_basic", last_session, {**kpis, **retest})

    return {**kpis, **retest}









def check_lateral_box(ticker):

    #df = load_ticker(ticker)
    df = load_serie(ticker)
    df = add_indicators(ticker, df)

    box = get_lateral_rectangle(ticker, df)
    return box
import logging
import pandas as pd
import json
import argparse

from finance.yfin.fetch_serie import load_serie
from finance.yfin.kpi import add_indicators, get_last_volatility, get_lateral_rectangle, detect_break_retest, adjust_dividents


logger = logging.getLogger(__name__)


def calculate_kpis(ticker):

    #df = load_ticker(ticker)
    df = load_serie(ticker)
    df = adjust_dividents(ticker, df)
    df = add_indicators(ticker, df)

    kpis = get_last_volatility(ticker, df)
    retest = detect_break_retest(ticker, df)

    return {**kpis, **retest}


def check_lateral_box(ticker):

    #df = load_ticker(ticker)
    df = load_serie(ticker)
    df = add_indicators(ticker, df)

    box = get_lateral_rectangle(ticker, df)
    return box
import logging
import pandas as pd
import json
import argparse

from finance.yfin.fetch import load_ticker
from finance.yfin.kpi import add_indicators, get_last_volatility, get_lateral_rectangle


logger = logging.getLogger(__name__)


def calculate_kpis(ticker):

    df = load_ticker(ticker)
    df = add_indicators(ticker, df)

    kpis = get_last_volatility(ticker, df)

    return kpis


def check_lateral_box(ticker):

    df = load_ticker(ticker)
    df = add_indicators(ticker, df)

    box = get_lateral_rectangle(ticker, df)
    return box
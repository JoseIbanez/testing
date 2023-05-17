#!/usr/bin/python
import time
import logging

from stock_price_bot.lib.common import configure_loger
from stock_price_bot.lib.model import Symbol
from stock_price_bot.lib.psql_link import Psql
from stock_price_bot.lib.yfinance_lib import get_symbol_info

logger = logging.getLogger(__name__)



def update_list():

    db = Psql()

    symbol_list = db.get_symbol_list()

    for s_id in symbol_list:
        s = get_symbol_info(s_id)
        db.update_symbol(s)

    return


def main():

    configure_loger()

    while True:
        try:
            update_list()
            logger.info("wait for other loop")
            time.sleep(300)

        except Exception as e:
            logger.fatal(e)
            time.sleep(300)


if __name__ == "__main__":
    main()

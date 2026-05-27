
"""
Save tickets in sqlite database as cache, to avoid hitting Yahoo Finance API too much.
"""

import sqlite3
import json
import logging
import time

logger = logging.getLogger(__name__)

FAST_INFO_TTL =  4 * 3600 
MORE_INFO_TTL = 24 * 3600 

class MyDBCache:
    def __init__(self):
        self.db_path = "./data/db/tickers.db"


    def get_fast_info(self, ticker):
        """
        Retrieve a ticker's fast_info from the database. Returns None if not found.
        fast_info is a JSON doc containing the fast_info data for the ticker.
        """


        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fast_info FROM tickers WHERE ticker=?", (ticker,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        fast_info_str = result[0] or "{}"
    
        try:
            fast_info = json.loads(fast_info_str) 
        except (json.JSONDecodeError, TypeError):
            logger.error("Error decoding JSON for ticker %s:%s",ticker,fast_info_str)
            return None

        if 'lastPrice' not in fast_info or 'yearHigh' not in fast_info or 'twoHundredDayAverage' not in fast_info:
            logger.warning("Incomplete fast_info for %s: %s", ticker, fast_info)
            return None


        update_ts = fast_info.get('update_ts',0)



        if update_ts < time.time() - FAST_INFO_TTL:
            logger.debug("Ticker %s has no update_ts in fast_info, treating as stale.", ticker)
            return None

        return fast_info





    def put_fast_info(self, ticker, fast_info):



        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO tickers (ticker) VALUES (?)", (ticker,))
        cursor.execute("UPDATE tickers SET fast_info_attempt=CURRENT_TIMESTAMP WHERE ticker=?", (ticker,))
        
        if fast_info:
            fast_info['update_ts'] = time.time()
            cursor.execute("UPDATE tickers SET fast_info=? WHERE ticker=?", (json.dumps(fast_info), ticker))


        conn.commit()
        conn.close()



    def get_more_info(self, ticker):
        """
        Retrieve a ticker's info from the database. Returns None if not found.
        info is a JSON doc containing the info data for the ticker.
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT more_info FROM tickers WHERE ticker=?", (ticker,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return None

        info_str = result[0] or "{}"
    
        try:
            info = json.loads(info_str) 
        except (json.JSONDecodeError, TypeError):
            logger.error("Error decoding JSON for ticker %s:%s",ticker,info_str)
            return None

        update_ts = info.get('update_ts',0)

        if update_ts < time.time() - MORE_INFO_TTL:
            logger.debug("Ticker %s has no update_ts in info, treating as stale.", ticker)
            return None

        return info
    

    def put_more_info(self, ticker, info):


        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO tickers (ticker) VALUES (?)", (ticker,))
        cursor.execute("UPDATE tickers SET more_info_attempt=CURRENT_TIMESTAMP WHERE ticker=?", (ticker,))
        if info:
            info['update_ts'] = time.time()
            cursor.execute("UPDATE tickers SET more_info=? WHERE ticker=?", (json.dumps(info), ticker))
        conn.commit()
        conn.close()



    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickers (
                ticker STRING PRIMARY KEY,
                tk_tv STRING,
                displayName STRING,
                sector STRING,
                volume INTEGER,
                currency STRING,
                hot INTEGER,
                hot_ts INTEGER,
                fast_info TEXT,
                fast_info_attempt TIMESTAMP,
                more_info TEXT,
                more_info_attempt TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()


    def set_ticker_info(self, ticker, info):
        """
        Update the displayName, sector, volume and currency for a ticker in the database.
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tickers
            SET displayName=?, sector=?, volume=?, currency=?, hot=?
            WHERE ticker=?
        """, (
            info.get("displayName") or info.get("longName"),
            info.get("sector"),
            info.get("volume"),
            info.get("currency"),
            info.get("hot", 0),
            ticker
        ))
        conn.commit()
        conn.close()


    def query_ticker_list(self):
        """
        Get the list of tickers from the database.
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT ticker FROM tickers where json_extract(fast_info, '$.lastPrice')>0 and hot>0 order by hot desc, volume desc;")
        result = cursor.fetchall()  
        conn.commit()
        conn.close()

        tickers = [row[0] for row in result]
        #logger.info("Queried ticker list from database: %s", tickers)  
        return tickers
    

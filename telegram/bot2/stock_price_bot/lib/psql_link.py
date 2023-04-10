#!/usr/bin/python
import psycopg2
from psycopg2.extras import RealDictCursor

import os
import logging

from stock_price_bot.lib.common import configure_loger
from stock_price_bot.lib.model import Symbol

logger = logging.getLogger(__name__)


class Psql():

    def __init__(self):

        database = "sp" 
        host = os.environ.get('DB_HOST','10.0.1.70')
        username = os.environ.get('DB_USERNAME','bot')
        password = os.environ.get('DB_PASSWORD','bopass')

        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password)

        with self.conn.cursor() as cur:
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)

    def close(self):
        self.conn.close()


    def db_read(self,sql,param):

        with self.conn.cursor() as cur:

            cur.execute(sql, param)
            result = cur.fetchall()

        logger.info(result)

    def update_symbol(self, s:Symbol):
        """
        yf_id           VARCHAR ( 50 ) UNIQUE NOT NULL,
        displayName     VARCHAR ( 80 ),
        marketState     VARCHAR ( 50 ),
        previousClose   NUMERIC( 10, 3),
        lastPrice       NUMERIC( 10, 3),
        currency        VARCHAR ( 50 ),
        _var            NUMERIC( 5, 2),
        _lastCheck      TIMESTAMP      
        """

        if not s:
            logger.error("Not symbol provied")
            return

        sql = """
        INSERT INTO symbol (yf_id, displayName, marketState, previousClose, lastPrice, currency, _var, _lastCheck)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW()) 
        ON CONFLICT (yf_id)
        DO UPDATE SET 
            displayName = %s,
            marketState = %s,
            previousClose = %s,
            lastPrice = %s,
            currency =%s,
            _var = %s,
            _lastCheck = NOW()
        ;
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, (s.id, s.displayName, s.marketState, s.previousClose, s.lastPrice, s.currency, s.priceVariation, 
                               s.displayName, s.marketState, s.previousClose, s.lastPrice, s.currency, s.priceVariation))

        self.conn.commit()
        logger.info("DB saved Symbol:%s",s.id)

        return

    def get_symbol_by_id(self,symbol_id:str) -> Symbol:


        s = Symbol()

        sql = "select * from symbol where yf_id = %s;"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql,(symbol_id,))
            record = cur.fetchone()

            s.id = record['yf_id']
            s.displayName = record['displayname'] 
            s.marketState = record['marketstate']
            s.previousClose = record['previousclose']      
            s.lastPrice = record['lastprice']
            s.currency = record['currency']
            s.priceVariation = record['_var']

        logger.info("DB fetched Symbol:%s",s.id)

        return s


    def get_symbol_list(self) -> list[str]:

        symbol_list = []

        sql = "SELECT DISTINCT yf_id FROM watcher;"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            for record in cur:
                s_id = record['yf_id']
                symbol_list.append(s_id)


        return symbol_list




    def get_symbol_changed(self,user_id) -> list[str]:

        symbol_list = []

        sql = """
        SELECT watcher.yf_id as s_id
        FROM watcher 
        JOIN symbol ON watcher.yf_id = symbol.yf_id
        WHERE user_id = %s
            AND (symbol.marketstate != 'CLOSED')
            AND (symbol._var > 1.00 or symbol._var < -1.00) 
            AND (var_last < _lastcheck::date or var_last IS NULL);
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (user_id,))
            for record in cur:
                s_id = record['s_id']
                symbol_list.append(s_id)


        return symbol_list


    def add_watcher(self, user_id:str, yf_id:str):
        """
        """


        sql = """
        INSERT INTO watcher (yf_id, user_id)
        VALUES (%s, %s) 
        ON CONFLICT (yf_id,user_id)
        DO NOTHING
        ;
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, (yf_id,user_id))

        self.conn.commit()
        logger.info("DB saved Watcher:%s-%s",user_id,yf_id)

        return


    def del_watcher(self, user_id:str, yf_id:str):
        """
        """


        sql = """
        DELETE FROM watcher
        WHERE yf_id = %s and user_id = %s
        ;
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, (yf_id,user_id))

        self.conn.commit()
        logger.info("DB removed Watcher:%s-%s",user_id,yf_id)

        return


    def done_watcher(self, user_id:str, yf_id:str):
        """
        """


        sql = """
        UPDATE watcher
        SET var_last = NOW()
        WHERE yf_id = %s and user_id = %s
        ;
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, (yf_id,user_id))

        self.conn.commit()
        logger.info("DB removed Watcher:%s-%s",user_id,yf_id)

        return


def main():

    configure_loger()

    db = Psql()

    s = Symbol()
    s.id = "VOD.L"
    s.displayName = "Vodafone"
    s.marketState = "CLOSED"
    s.previousClose = 230.33
    s.lastPrice = 231.55
    s.currency = "GBp"
    s.priceVariation = 2.33

    db.update_symbol(s)

    s2 = db.get_symbol_by_id(s.id)
    print(s2)

    user_id = "2322"
    l1 = db.get_symbol_changed(user_id)
    print(l1)

    db.add_watcher(user_id,"SAN.MC")
    db.add_watcher(user_id,"DIS")

    l1 = db.get_symbol_changed(user_id)
    print(l1)

    db.del_watcher(user_id,"ITX.MC")

if __name__ == "__main__":
    main()

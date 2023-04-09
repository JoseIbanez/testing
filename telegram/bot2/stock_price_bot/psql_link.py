#!/usr/bin/python
import psycopg2
import os

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

    def db_read(self,sql,param):


        with self.conn.cursor() as cur:

            cur.execute(sql, param)
            result = cur.fetchall()

        print(result)


def main():

    db = Psql()

    db.db_read("select * from symbol;",[])


if __name__ == "__main__":
    main()

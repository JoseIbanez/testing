#!/usr/bin/python
import MySQLdb
import time
import datetime


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",             # your username
                     passwd="VFhcs123!",  # your password
                     db="fruit")          # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cursor = db.cursor()


cust   = "Cust16"
kpi    = "RegisteredPhones"
domain = "/"
value  = 10
date   = "2016-10-01"

#Loop
while (1):

        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	value=value+1
        time.sleep(1)
 
        print value

        cursor.execute("""
                Insert into log
                  (cust,kpi,domain,value,date)
                  values
                  (%s,%s,%s,%s,%s);
                """,
                (cust,kpi,domain,value,date))
        #"""


        cursor.execute("""
                Insert ignore into kpi 
                  (cust,kpi,domain)
                  values
                  (%s,%s,%s)
                """,
                (cust,kpi,domain))
        #"""


        cursor.execute("""
                update kpi
                set
                  value=%s,
                  date=%s
                where
                  cust=%s and kpi=%s and domain=%s
                """,
                (value,date,cust,kpi,domain))
        #"""

        db.commit()


        print cust, kpi, domain, value, date


	if (value>200):
	   break


# print all the first cell of all the rows

db.close()

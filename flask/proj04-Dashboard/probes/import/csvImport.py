#!/usr/bin/python
import MySQLdb
import time
import datetime
import os
import csv
import sys, getopt


inputfile = ''

#
#
#
def main(argv):
   global inputfile
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'csvImport.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'csvImport.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

#
#
####

main(sys.argv[1:])

myhost = os.environ.get('BDB_MYSQL_HOST')
myuser = os.environ.get('BDB_MYSQL_USER')
mypass = os.environ.get('BDB_MYSQL_PASS')
mydb   = os.environ.get('BDB_MYSQL_DB')



db = MySQLdb.connect(host=myhost,    # your host, usually localhost
                     user=myuser,    # your username
                     passwd=mypass,  # your password
                     db=mydb)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cursor = db.cursor()


with open(inputfile, 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=',')
   for row in reader:

        cust=row[0]
	kpi=row[1]
        domain=row[2]
        value=row[3]
        date=row[4]

        #date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#value=value+1
        #time.sleep(1)

        print cust, kpi, domain, value, date

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



# print all the first cell of all the rows
db.close()

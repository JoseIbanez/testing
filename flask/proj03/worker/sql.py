#!/usr/bin/python

import mysql.connector
import json
import collections


cnx = mysql.connector.connect(user='root',password='passw0rd', host='127.0.0.1', database='fruit');

cursor = cnx.cursor()
cursor.execute("""
            Select date,dc1,dc2
            From hDateDevices
            """)
rows = cursor.fetchall()
#desc = cursor.description

oList=[]
for row in rows:
    d = collections.OrderedDict()
    d['date']=row[0].strftime("%Y-%m-%d")
    d['dc1']=row[1]
    d['dc2']=row[2]
    oList.append(d)

j = json.dumps(oList)
print j

cnx.close();

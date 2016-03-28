#!/usr/bin/python3

from pymongo import MongoClient
client = MongoClient("rs01/m1,m2,m3")

db=client['test']
collection=db['inventory']

for item in collection.find():
   print(item)

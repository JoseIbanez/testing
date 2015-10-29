#!/usr/bin/python
import boto.ses
import boto.dynamodb2
from boto.dynamodb2.table import Table

conn = boto.dynamodb2.connect_to_region(
    'eu-west-1'
)

users = Table('CMR', connection=conn)

data = users.get_item(node='ccm1',date='2014-01-01')

print data
print data['date'],data['a_number']

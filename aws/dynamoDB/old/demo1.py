#!/usr/bin/python
import boto.ses
import boto.dynamodb2
from boto.dynamodb2.table import Item
from boto.dynamodb2.table import Table
import random
import string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


conn = boto.dynamodb2.connect_to_region(
    'eu-west-1'
)

users = Table('CMR', connection=conn)

data = users.get_item(node='ccm1',date='2014-01-02')

print data
print data['date'],data['a_number'],data['duration']

data['duration']=data['duration']+random.randint(1,5)

data.save()

node=id_generator()

dato2 = Item(users, data= {
    'node': node,
    'date': '2015-01-01',
    'duration': 3
})

dato2.save()

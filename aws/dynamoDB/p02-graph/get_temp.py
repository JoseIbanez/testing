#!/usr/bin/env python

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            #return str(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)



dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('temp')

print("reading last values")

response = table.query(
    ProjectionExpression="probe, #date, #temp",
    #ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
    ExpressionAttributeNames={ "#date": "date", "#temp": "temp" },
    KeyConditionExpression=Key('probe').eq("b827eb.7c3714.c1") & 
                           Key('date').between('2017-08-09', '2017-08-10')
)

for i in response[u'Items']:
    #print(json.dumps(i, cls=DecimalEncoder))
    print i['date']+','+i['probe']+','+str(i['temp'])

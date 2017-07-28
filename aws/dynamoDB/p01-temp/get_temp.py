#!/usr/bin/env python

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)



dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('temp')

print("reading last values")

response = table.query(
    ProjectionExpression="probe, #date, #temp",
    #ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
    ExpressionAttributeNames={ "#date": "date", "#temp": "temp" },
    KeyConditionExpression=Key('probe').eq("28-0414517b55ff") & Key('date').between('2017-07-28', '2017-07-30')
)

for i in response[u'Items']:
    print(json.dumps(i, cls=DecimalEncoder))
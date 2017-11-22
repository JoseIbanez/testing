#!/usr/bin/env python

import boto3
import json
import decimal
#import datetime
from datetime import date, timedelta, datetime
import argparse
from boto3.dynamodb.conditions import Key, Attr


#Madrid   b827eb.7c3714.c1
#Siguenza b827eb.61eb84.c3

parser = argparse.ArgumentParser(
    description='Request any Twitter Streaming or REST API endpoint')
parser.add_argument(
    '-probe',
    type=str,
    help='Probe id',
    default="b827eb.7c3714.c1")
parser.add_argument(
    '-date',
    type=str,
    help='Last date of the graph')
parser.add_argument(
    '-hours',
    type=int,
    help='Number of previous hours',
    default=24)
args = parser.parse_args()


try:
    lastDate = datetime.strptime(args.date, "%Y-%m-%d")
except:
    lastDate = datetime.today() - timedelta(1)

lastDate=lastDate + timedelta(hours=24)
initialDate=lastDate - timedelta(hours=args.hours)

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
print(initialDate.strftime("%Y-%m-%d"))
print(lastDate.strftime("%Y-%m-%d"))

response = table.query(
    ProjectionExpression="probe, #date, #temp, humidity",
    ExpressionAttributeNames={"#date": "date", "#temp": "temp"},
    KeyConditionExpression=Key('probe').eq(args.probe) &
                           Key('date').between(initialDate.strftime("%Y-%m-%d"),
                                               lastDate.strftime("%Y-%m-%d"))
)

for i in response[u'Items']:
    #print(json.dumps(i, cls=DecimalEncoder))
    if 'humidity' in i.keys():
        print i['date']+','+i['probe']+','+str(i['temp'])+','+str(i['humidity'])
    else:
        print i['date']+','+i['probe']+','+str(i['temp'])+',None'
        
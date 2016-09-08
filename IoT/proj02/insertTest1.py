#!/usr/bin/python2.7

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import sys

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


## Connect with DB

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
#, endpoint_url="http://localhost:8000")
table = dynamodb.Table('KumoDB')


## Loop in stdin
while True:
    line=sys.stdin.readline().rstrip('\n')
    (probe,date,temp)=line.split(",")
    print(line)

    response = table.put_item(
       Item={
            'date': date,
            'probe': probe,
            'temp': temp
            }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

print("End")

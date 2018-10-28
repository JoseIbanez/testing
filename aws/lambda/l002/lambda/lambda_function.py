#!/usr/bin/env python
import logging
import boto3
import json
import decimal
from datetime import date, timedelta, datetime
from boto3.dynamodb.conditions import Key, Attr

#logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def adefault(self, o):
        if isinstance(o, decimal.Decimal):
            #return str(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    ret = getTemp()

    return {
        "statusCode": 200,
        "body": json.dumps(ret)
    }

def getTemp():

    probe = "b827eb.300520.c3"
    hours = 48

    lastDate = datetime.today()
    lastDate = lastDate + timedelta(hours=24)
    initialDate = lastDate - timedelta(hours=hours)



    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('temp')

    print("reading last values")
    print(initialDate.strftime("%Y-%m-%d"))
    print(lastDate.strftime("%Y-%m-%d"))

    response = table.query(
        ProjectionExpression="probe, #date, #temp, humidity",
        ExpressionAttributeNames={"#date": "date", "#temp": "temp"},
        KeyConditionExpression=Key('probe').eq(probe) &
                               Key('date').between(initialDate.strftime("%Y-%m-%d"),
                                                   lastDate.strftime("%Y-%m-%d"))
    )


    #print response[u'Items']

    #print "-------------------------------------"

    list=[]

    for i in response[u'Items']:
        #print(json.dumps(i, cls=DecimalEncoder))
        if 'humidity' in i.keys():
            #print i['date']+','+i['probe']+','+str(i['temp'])+','+str(i['humidity'])
            item = { "date": i['date'],
                     "temp": int(i['temp']),
                     "humidity": int(i['humidity']) }
        else:
            #print i['date']+','+i['probe']+','+str(i['temp'])+',None'
            item = { "date": i['date'],
                     "temp": int(i['temp']) }

        list.append(item)


    out = { "probe": probe, "data": list }

    return out


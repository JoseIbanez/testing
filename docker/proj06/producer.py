#!/usr/bin/env python

import sys
import os
import time
import boto3

try:
    region = os.environ['REGION']
    queue_url = os.environ['QUEUE']
except:
    print "Enviroment variables not availables"
    sys.exit()


# Create SQS client
sqs = boto3.client('sqs', region_name = region)

print sqs

#queue_url = 'https://sqs.eu-west-1.amazonaws.com/532272748741/test01'

counter = 20
while True:

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )

    print(response['MessageId'])
    time.sleep(2)

    counter = counter - 1
    if counter < 0:
        sys.exit()


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

counter = 0

while True:

    print "Menssage counter "+str(counter)

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    
    if not 'Messages' in response:
        print "No messages"
        time.sleep(10)
        #sys.exit()
        continue
    
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
    counter = counter + 1

    time.sleep(10)
    continue


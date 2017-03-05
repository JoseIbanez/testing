#!/usr/bin/env python


import json
import boto3

arn="arn:aws:sns:eu-west-1:532272748741:Teste"
client = boto3.client('sns')


message = {"foo": "bar1"}
response = client.publish(
    TargetArn=arn,
    Message=json.dumps({'default': json.dumps(message)}),
    MessageStructure='json'
)

message = {"foo": "bar2"}
response = client.publish(
    TargetArn=arn,
    Message=json.dumps({'default': json.dumps(message)}),
    MessageStructure='json'
)

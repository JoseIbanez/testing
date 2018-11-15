import logging
import time
import json
import uuid
import datetime
import sys
import boto3

client = boto3.client(service_name='iot-data',
                      endpoint_url='https://a1o7eza7uxtx5n-ats.iot.eu-west-1.amazonaws.com',
                      )

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def set_thing_state(thingName, property, state):

    payload = json.dumps({'state': { 'desired': { property : state } }})
    
    logger.info("IOT update, thingName:"+thingName+", payload:"+payload)

    response = client.update_thing_shadow(
        thingName = thingName, 
        payload =  payload
        )

    logger.info("IOT response: " + str(response))  
    logger.info("Body:"+response['payload'].read())


def get_thing_state(thingName, property):

    response = client.get_thing_shadow(thingName=thingName)
    
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())

    logger.info("IOT response: " + str(jsonState))  

    ret = jsonState["state"]["reported"][property]
    return ret



####################
# Setup logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

logger.setLevel(logging.INFO)


set_thing_state("h02-001", "fuego", "on")

print ""
print "#########"
print ""

ret = get_thing_state("h02-001", "fuego")
print ret

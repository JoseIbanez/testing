import logging
import time
import json
import uuid
import datetime

import boto3

client = boto3.client('iot-data')

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def light_state(state):
    # Change topic, qos and payload
    response = client.update_thing_shadow(
        thingName = 'Your-Thing-Name', 
        payload = json.dumps({
            'state': {
                'desired': {
                    'light': state
                }
            }
            }
            )
        )

def get_uuid():
    return str(uuid.uuid4())
    
# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info("Received v3 directive!")

    logger.info(json.dumps(event))
    
    if event['directive']['header']['name'] == "Discover":
        logger.info("Discover")
        response = handle_discovery(event)
    else:
        logger.info("Control")
        response = handle_control(event, context)    

    logger.info("response" + json.dumps(response))  
    return response



def handle_discovery(event):

    response = {
        "event" : {
            "header" : {
                "correlationToken": "12345692749237492",
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": event['directive']['header']['messageId']
            },
            "payload" : {
                "endpoints":[
                    {
                        "endpointId": "your_custom_endpoint",
                        "manufacturerName": "Manufacturer 1234",
                        "friendlyName": "Your Light Name",
                        "description": "Smart Device Switch",
                        "displayCategories": [ "SWITCH" ],
                        "cookie": {
                            "key1": "arbitrary key/value pairs for skill to reference this endpoint.",
                        },
                        "capabilities": [
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa",
                                "version": "3"
                            },
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa.PowerController",
                                "version": "3",
                                "properties": {
                                    "supported": [ { "name": "powerState" } ],
                                    "proactivelyReported": True,
                                    "retrievable": True
                                }
                            }
                        ]
                    }
                ]
            }
        }  
    }
    logger.info("Response: " +json.dumps(response))

    ####################
    request = event
    
    switchCapabilities = [
        {
            "type": "AlexaInterface",
            "version": "3",
            "interface": "Alexa"
        },
        {
            "type": "AlexaInterface",
            "version": "3",
            "interface": "Alexa.PowerController",
            "properties": {
                "supported": [ { "name": "powerState" } ],
                "proactivelyReported": True,
                "retrievable": True
            }
        }
    ]


    header = request.directive.header
    header.name = "Discover.Response"

    sw1 = {
        "endpointId": "your_custom_endpoint",
        "manufacturerName": "Manufacturer 1234",
        "friendlyName": "Your Light Name",
        "description": "Smart Device Switch",
        "displayCategories": [ "SWITCH" ],
        "cookie": {
            "key1": "arbitrary key/value pairs for skill to reference this endpoint.",
        },
        "capabilities": switchCapabilities
    }

    sw2 = {
        "endpointId": "your_custom_endpoint",
        "manufacturerName": "Manufacturer 1234",
        "friendlyName": "Your Light Name",
        "description": "Smart Device Switch",
        "displayCategories": [ "SWITCH" ],
        "cookie": {
            "key1": "arbitrary key/value pairs for skill to reference this endpoint.",
        },
        "capabilities": switchCapabilities
    }


    response = { 
        "event" : { 
            "header" : header, 
            "payload" : {
                "endpoints" : [ sw1, sw2 ]
            } 
        }
    }


    return response
 




def handle_control(request, context):
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]

    if request_namespace == "Alexa.PowerController":
        if request_name == "TurnOn":
            light_state("on")
            value = "ON"
        else:
            light_state("off")
            value = "OFF"

        response = {
            "context": {
                "properties": [
                    {
                        "namespace": "Alexa.PowerController",
                        "name": "powerState",
                        "value": value,
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    }
                ]
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": get_uuid(),
                    "correlationToken": request["directive"]["header"]["correlationToken"]
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": "access-token-from-Amazon"
                    },
                    "endpointId": request["directive"]["endpoint"]["endpointId"]
                },
                "payload": {}
            }
        }
        return response
    
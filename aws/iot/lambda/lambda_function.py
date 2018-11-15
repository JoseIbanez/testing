import logging
import time
import json
import uuid
import datetime

import boto3

client = boto3.client('iot-data')


########### AUX ###############################

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())


########## IOT-DATA ###########################
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



################################################
    
# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info("Received v3 directive!")
    logger.info(json.dumps(event))
    
    if event['directive']['header']['name'] == "Discover":
        logger.info("Discover")
        response = handle_discovery(event)
        
    elif event['directive']['header']['name'] == "ReportState":
        logger.info("ReportState")
        response = handle_report(event)

    else:
        logger.info("Control")
        response = handle_control(event, context)    

    logger.info("response: " + json.dumps(response))  
    return response


def handle_report(request):

    header = request['directive']['header']
    header['name'] = "StateReport"
    endpoint = request['directive']['endpoint']

    context = {
        "properties": [
            {

                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": "ON",
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 500
            }
        ]
    }

    ###

    response = { 
        "context" : context,
        "event" : { 
            "header" : header, 
            "endpoints" : endpoint,
            "payload" : {}
        }
    }

    return response

    
    


def handle_discovery(request):
    
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
                "retrievable": True
            }
        }
    ]


    header = request['directive']['header']
    header['name'] = "Discover.Response"

    sw1 = {
        "endpointId": "h2_001_ch1",
        "manufacturerName": "Linux",
        "friendlyName": "Camara",
        "description": "Mi cosa camara",
        "displayCategories": [ "SWITCH" ],
        "cookie": {
            "key1": "h2-001",
            "key2": "ch1"
        },
        "capabilities": switchCapabilities
    }

    sw2 = {
        "endpointId": "h2_001_ch2",
        "manufacturerName": "Linux",
        "friendlyName": "Fuego",
        "description": "Mi cosa fuego",
        "displayCategories": [ "SWITCH" ],
        "cookie": {
            "key1": "h2-001",
            "key2": "ch2"
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
            set_thing_state("h02-001","camara","on")
            value = "ON"
        else:
            set_thing_state("h02-001","camara","off")
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
    
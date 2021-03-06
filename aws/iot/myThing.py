'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
#import argparse
from os.path import expanduser
import yaml
import socket               # Import socket module
import thread
import sys
import subprocess

# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print("++++++++DELTA++++++++++")
    print("Payload: "+ str(payload))
    print("responseStatus: "+str(responseStatus))
    print("token: "+str(token))
    payloadDict = json.loads(payload)
    print("state: " + str(payloadDict["state"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")

    try:
        state = payloadDict["state"]
    except:
        print("No property received")
        return

    ansState = controlerMapping(state)
    if not ansState:
        return

    try:
        JSONPayload = {"state":{"reported": state }}
        print("Reporting: "+str(JSONPayload))
        deviceShadowHandler.shadowUpdate(json.dumps(JSONPayload), None, 5)
        #time.sleep(5)
        #JSONPayload = {"state":{"reported":{"property": 0 }}}
        #deviceShadowHandler.shadowUpdate(json.dumps(JSONPayload), None, 5)
    except:
        print("report error")


def controlerMapping(reqState):

    myMap = {
        "camara:on"  : { "socket": "bash",          "order" : "/home/ibanez/Projects/testing/youtube/stream2youtube.sh" },
        "camara:off" : { "socket": "bash",          "order" : "killall ffmpeg" },
        "fuego:on"   : { "socket": "bash",          "order" : "touch /tmp/fuego.tmp" },
        "fuego:off"  : { "socket": "bash",          "order" : "touch /tmp/fuego.tmp" },
        ".fuego:on"  : { "socket": "/tmp/channel0", "order" : "camara on" },
        ".fuego:off" : { "socket": "/tmp/channel0", "order" : "fuego on"}
    }

    retState = {}

    for key in reqState:

        orderId = key+":"+str(reqState[key])
        orderObj = myMap.get(orderId)

        if not orderObj:
            print "Command not defined"
            continue

        socket = orderObj.get('socket')
        order  = orderObj.get('order')

        if socket == "bash":

            print order
            try:
                subprocess.Popen(order.split())
                retState[key] = reqState[key]
            except:
                print sys.exc_info()[0]
                


    return retState



def controlerMapping_old(reqState):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect("/tmp/channel0")
    except:
        print("socket error")
        return None

    for key in reqState:

        orderId = key+":"+str(reqState[key])
        orderObj = myMap.get(orderId)

        if not orderObj:
            print "Command not defined"
            continue

        s.send(orderObj.get('order'))
        data = s.recv(1024)
        print("socket data: "+data)

    s.close()
    return reqState








# Read in config-file parameters
configFile = "~/.secrets/iot/iot-config.yml"
try:
    with open(expanduser(configFile), 'r') as stream:
        config = yaml.load(stream)
except yaml.YAMLError as exc:
        print exc

host = config.get('host')
rootCAPath = expanduser(config.get('rootCAPath'))
certificatePath = expanduser(config.get('certificatePath'))
privateKeyPath = expanduser(config.get('privateKeyPath'))
thingName = config.get('thingName')
clientId = config.get('clientId')
port = 8883


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)


# Loop forever
while True:
    time.sleep(1)

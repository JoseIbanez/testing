#!/bin/bash

# https://github.com/aws/aws-iot-device-sdk-python
# https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html#server-authentication
# https://www.hackster.io/ben-eagan/alexa-controlled-leds-through-arduino-yun-ac1171

sudo apt-get install python-pip

pip install awscli AWSIoTPythonSDK
mkdir -p ~/.secrets/iot
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem -P ~/.secrets/iot/
wget https://www.amazontrust.com/repository/AmazonRootCA2.pem -P ~/.secrets/iot/


aws iot-data get-thing-shadow    --thing-name v01 o.txt && cat o.txt
aws iot-data update-thing-shadow --thing-name v01     --payload '{"state":{"desired":{"color":"green"}}}' o.log
aws iot-data update-thing-shadow --thing-name h02-001 --payload '{"state":{"desired":{"property":33}}}' o.log



ffmpeg -i /dev/video0 -f alsa -ac 1 -i plughw:1,0 -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental \
    -f flv rtmp://a.rtmp.youtube.com/live2/$CHANNELID

#!/bin/bash

# https://github.com/aws/aws-iot-device-sdk-python
# https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html#server-authentication
sudo apt-get install python-pip

pip install awscli AWSIoTPythonSDK
mkdir -p ~/.secrets/iot
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem -P ~/.secrets/iot/
wget https://www.amazontrust.com/repository/AmazonRootCA2.pem -P ~/.secrets/iot/


aws iot-data get-thing-shadow    --thing-name v01 o.txt && cat o.txt
aws iot-data update-thing-shadow --thing-name v01 --payload '{"state":{"desired":{"color":"green"}}}' o.txt
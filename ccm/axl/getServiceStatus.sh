#!/bin/bash

node=$1
query="GetServiceStatus.xml"
answer="./answers/serviceStatus"

curl -k -n  \
	-H "Content-type: text/xml;" \
	-d @"./queries/$query" \
	https://$node:8443/controlcenterservice2/services/ControlCenterServices 
	 > "$answer.$node.xml" 

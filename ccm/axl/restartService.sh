#!/bin/bash

node=$1
service=$2
query="ControlServiceRequest.xml"
answer="./answers/ServiceRestart"

cp ./queries/$query /tmp/
sed -i 's/{{}}/$service/g' /tmp/$query

curl -k -n  \
	-H "Content-type: text/xml;" \
	-d @/tmp/$query https://$node:8443/controlcenterservice2/services/ControlCenterServices \
	 > "$answer.$node.xml" 2>/dev/null


xmllint --format "$answer.$node.xml"

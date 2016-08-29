#!/bin/bash

node=$1
query="GetServiceStatus.xml" 
answer="./answers/serviceStatus" 
tmpAnswer="$answer-$node" 
log="./log/axl.log"
options="--interface eth2"

curl -k -n $options  \
	-H "Content-type: text/xml;" \
	-d @"./queries/$query" \
	https://$node:8443/controlcenterservice2/services/ControlCenterServices \
	> ${tmpAnswer} 2>>$log

cat ${tmpAnswer} >> $log
xmllint --format ${tmpAnswer} > ${tmpAnswer}.xml
cat ${tmpAnswer}.xml >>$log

sed -i 's/ns1://g' ${tmpAnswer}.xml 
xml2csv --input ${tmpAnswer}.xml --output ${tmpAnswer}.csv --tag item

cat ${tmpAnswer}.csv | sed 's/"//g' | sort -t , -k 6 -n > ${tmpAnswer}.sorted.csv

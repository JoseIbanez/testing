#!/bin/bash

node=$1
query="GetServiceStatus.xml" 
answer="./answers/serviceStatus" 
tmpAnswer="$answer-$node" 
log="./log/axl.log"
#options="--interface eth2"
options=""

function sendQuery {
  node=$1
  tmpAnswer="$answer-$node"

  printf ">> node:$1, answerFile:$tmpAnswer.\n"
  echo "null" >  ${tmpAnswer}.csv
  echo "null" >  ${tmpAnswer}.sorted.csv
  
  
  curl -k -n $options  \
  	-H "Content-type: text/xml;" \
  	-d @"./queries/$query" \
  	https://$node:8443/controlcenterservice2/services/ControlCenterServices \
  	> ${tmpAnswer} 2>>$log
  
  cat ${tmpAnswer} >> $log
  xmllint --format ${tmpAnswer} > ${tmpAnswer}.xml
  cat ${tmpAnswer}.xml >>$log
  
  sed -i 's/ns1://g' ${tmpAnswer}.xml 
  xml2csv --input ${tmpAnswer}.xml --output ${tmpAnswer}.csv --tag item >> $log
  
  cat ${tmpAnswer}.csv | sed 's/"//g' | sort -t , -k 6 -n > ${tmpAnswer}.sorted.csv
}

function show_help {
  echo "TBD"
  exit
}

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:

verbose=0
service=""

while getopts "h?vn:s:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  verbose=1
        ;;
    n)  node=$OPTARG
        ;;
    s)  service=$OPTARG
        ;;
    esac
done

if [ "${node}" ]; then
  sendQuery "${node}" "${service}" &
  exit
fi


while read node; do
  sendQuery "${node}" "${service}" &
  sleep 1
done

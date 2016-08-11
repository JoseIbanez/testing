#!/bin/bash

query="ControlServiceRequest"
answer="./answers/ServiceRestart"
log="./log/axl.log"


function sendQuery {

  node=$1
  service=$2
  tmpQuery="/tmp/$query-$node.xml"
  tmpAnswer="$answer-$node.xml"

  printf "\n\nStart node:$1, service:$2.\n" >> $log
  date >> $log

  printf ">> node:$1, service:$2, answerFile:$tmpAnswer.\n"
  date

  cp ./queries/$query.xml $tmpQuery
  sed -i "s/{{service}}/$service/g" $tmpQuery

  cat $tmpQuery >> $log

  #rm $tmpAnswer
  curl -k -n  \
	-H "Content-type: text/xml;" \
	-d @$tmpQuery https://$node:8443/controlcenterservice2/services/ControlCenterServices \
	 > ${tmpAnswer} 2>>$log

  #rm $tmpQuery
  cat $tmpAnswer >> $log
  xmllint --format $tmpAnswer >>$log

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

if [ -z "${service}" ]; then
  show_help
  exit
fi


if [ "${node}" ]; then
  sendQuery "${node}" "${service}" &
  exit
fi


while read node; do
  sendQuery "${node}" "${service}" &
  sleep 2
done



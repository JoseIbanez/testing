#!/bin/sh
path=$2
name=$1

while [ 1 ] 
do
   t=`cat "$path/w1_slave" | grep 't=' | cut -d '=' -f 2`
   d=`date -Iseconds`
   m="$name,$d,$t"
   echo $m
   mosquitto_pub -h broker.hivemq.com -t /ibanez/temp1 -m "$m"
   unset m
   sleep 60
done

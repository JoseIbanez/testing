#!/bin/sh
touch /etc/enviroment
COREOS_PRIVATE_IPV4=`/bin/ifconfig eth0 | grep "inet " | awk  '{print $2}'`
echo "COREOS_PRIVATE_IPV4" $COREOS_PRIVATE_IPV4  | tee /etc/enviroment



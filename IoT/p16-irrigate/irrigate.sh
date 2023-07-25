#!/bin/bash

topic="q/ESP3C71BF51A064"

/usr/bin/mosquitto_pub -t $topic -m "0020;0001" ; sleep  5
/usr/bin/mosquitto_pub -t $topic -m "0015;1001" ; sleep 15




for i in $(seq 1 6); do

  echo $i
  /usr/bin/mosquitto_pub -t $topic -m "0015;0001"
  sleep 10
  /usr/bin/mosquitto_pub -t $topic -m "0010;1001"
  sleep 8

done

/usr/bin/mosquitto_pub -t $topic -m "0002;0001"




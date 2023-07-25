#!/bin/bash

topic="q/ESP3C71BF51A064"

/usr/bin/mosquitto_pub -t $topic -m "0020;0001" ; sleep 10
/usr/bin/mosquitto_pub -t $topic -m "0010;0101" ; sleep 15




for i in $(seq 1 3); do

  echo $i
  /usr/bin/mosquitto_pub -t $topic -m "0012;0001"
  sleep 10
  /usr/bin/mosquitto_pub -t $topic -m "0005;0101"
  sleep 3

done

/usr/bin/mosquitto_pub -t $topic -m "0002;0001"



#!/bin/bash

tc qdisc add dev eth0 root tbf rate 100mbit burst 40mbit latency 400ms
tc qdisc show dev eth0

useradd -u 1000 acelink

/usr/bin/supervisord

runuser -u acelink /acelink/internal-hls.sh

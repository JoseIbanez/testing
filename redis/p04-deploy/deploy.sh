#!/bin/bash

sudo apt-get update
sudo apt-get install redis-server -y

#update hosts file
myIP=`ifconfig | grep -A 1 Ethernet | grep inet | sed 's/.*addr://g' | sed 's/ *Bcast:.*//g'`
echo "$myIP  redis" | sudo tee -a /etc/hosts
cat /etc/hosts



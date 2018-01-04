#!/bin/bash

sudo apt-get update
sudo apt-get install redis-server -y

sudo service redis-server start

#reconfig redis to accept external binds
sudo sed -i "s/^bind .*/bind 0.0.0.0/" /etc/redis/redis.conf
sudo service redis-server restart

#update hosts file
myIP=`ifconfig | grep -A 1 Ethernet | grep inet | sed 's/.*addr://g' | sed 's/ *Bcast:.*//g'`
echo "$myIP  redis" | sudo tee -a /etc/hosts
cat /etc/hosts

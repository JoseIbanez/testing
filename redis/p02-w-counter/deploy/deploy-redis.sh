#!/bin/bash

sudo apt-get update
sudo apt-get install redis-server -y

sudo service redis-server start

#reconfig redis to accept external binds
sudo sed -i "s/^bind .*/bind 0.0.0.0/" /etc/redis/redis.conf
sudo service redis-server restart


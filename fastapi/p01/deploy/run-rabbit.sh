#!/bin/bash

grep -q 'redis' /etc/hosts  || echo '127.0.0.1 redis rabbitmq postgres' | sudo tee -a /etc/hosts


sudo docker pull redis
sudo docker pull rabbitmq:3-management

sudo docker run -d -p 6379:6379 redis

#docker run -d -p 5672:5672 -p 25672:25672 rabbitmq
sudo docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

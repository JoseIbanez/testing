#!/bin/bash

docker run -d -p 6379:6379 redis
docker run -d -p 5672:5672 rabbitmq

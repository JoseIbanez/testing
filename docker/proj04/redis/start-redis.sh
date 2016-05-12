#!/bin/sh

docker run --name redis01 -d redis:alpine
docker inspect redis01 | jq -r '.[].NetworkSettings.IPAddress' > ./redis.lst

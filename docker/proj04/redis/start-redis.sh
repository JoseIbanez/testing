#!/bin/sh

docker run --name redis01 --net=my-net-01 -d redis:alpine
docker inspect redis01 | jq -r '.[].NetworkSettings.Networks."my-net-01".IPAddress' > ./redis.lst
cp redis.lst ../worker/

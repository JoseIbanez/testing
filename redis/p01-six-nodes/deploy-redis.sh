#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y redis-server net-tools
sudo systemctl stop redis-server
sudo systemctl disable redis-server.service

rm -rf 700*
export PORT
for PORT in $(seq 7000 7005 ); do
    mkdir -p $PORT
    envsubst < redis.conf > $PORT/redis.conf
done


for PORT in $(seq 7000 7005 ); do
    cd $PORT
    ls
    screen -dmS "redis$PORT" redis-server redis.conf
    cd ..
done



NODELIST=""
IP="10.39.122.21"

for i in $(seq 7000 7005 ); do
    NODELIST="${NODELIST} $IP:$i"
done
echo $NODELIST

set -x
redis-cli --cluster create $NODELIST --cluster-replicas 1 --cluster-yes
set +x

redis-cli --cluster check $IP:7000
redis-cli --cluster info  $IP:7000


redis-cli -c -p 7000 <<EOF
CLUSTER NODES
CLUSTER INFO

SET mykey6 "value red" EX 20
SET mykey1 "value blue" EX 20
SET mykey3 "value green" EX 20

GET mykey1
GET mykey3
GET mykey6

EOF


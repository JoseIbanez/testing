#!/bin/sh

get_ip() {
    nslookup $1 | grep -A 2 Name: | grep Address: | cut -d' ' -f2
}

sleep 10
BASENAME="redis-cluster-redis-node"
CLUSTER_SIZE=6


for i in $(seq 1 $CLUSTER_SIZE); do
    NODELIST="${NODELIST} $(get_ip $BASENAME-$i):6379"
done

set -x
redis-cli --cluster create $NODELIST --cluster-replicas 1 --cluster-yes
set +x

while true; do
    redis-cli --cluster check "redis-node:6379"    
    redis-cli --cluster info  "redis-node:6379"    
    sleep 60
done
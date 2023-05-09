#!/bin/sh

get_ip() {
    nslookup -type=a $1 | grep -A 2 Name: | grep Address: | cut -d' ' -f2
}

echo "** start redis cluster config **"
sleep 20
BASENAME="redis-cluster"
DOMAIN=$(cat /etc/resolv.conf | grep search | cut -d' ' -f2)
MAX_NODE=5
NODELIST=""

for i in $(seq 0 $MAX_NODE); do
    HOSTNAME="$BASENAME-$i.$BASENAME.$DOMAIN"
    ping -c 3 $HOSTNAME
    NODELIST="${NODELIST} $(get_ip $HOSTNAME):6379"
done
echo $NODELIST

set -x
redis-cli --cluster create $NODELIST --cluster-replicas 1 --cluster-yes
set +x

while true; do
    redis-cli --cluster check "$BASENAME:6379"
    redis-cli --cluster info  "$BASENAME:6379"
    sleep 60
done

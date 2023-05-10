#!/bin/sh

get_ip() {
    nslookup -type=a $1 | grep -A 2 Name: | grep Address: | cut -d' ' -f2
}


remove_failed_nodes() {

    HOSTNAME=$1
    MAX_NODE=5

    # Remove failed nodes
    FAILED=$(redis-cli -c -h $HOSTNAME -p 6379 CLUSTER NODES | grep fail | cut -d' ' -f 1); 
    echo "Failed nodes: $FAILED"
    for n in $FAILED; do 
        echo "Remove failed Node: $n"

        for i in $(seq 0 $MAX_NODE); do
            NODENAME="$BASENAME-$i.$BASENAME.$DOMAIN"
            redis-cli -c -h $NODENAME -p 6379 CLUSTER FORGET $n

        done

    done


    # Save a valid node 
    OTHER=$(redis-cli -c -h $HOSTNAME -p 6379 CLUSTER NODES | grep -v slave | grep -v myself | head -n 1 | cut -d' ' -f2 | cut -d '@' -f1)
    if [ -n "$OTHER" ]; then
        echo $OTHER > /tmp/other_node
    fi

}


add_new_node() {

    HOSTNAME=$1

    HOSTURL="$(get_ip $HOSTNAME):6379"

    # Add new nodes
    NEWNODE=$(redis-cli -c -h $HOSTNAME -p 6379 CLUSTER NODES | grep -v myself)
    OTHER=$(cat /tmp/other_node)
    if [ -z "$NEWNODE" ] && [ -n "$OTHER" ]; then
        echo "Adding new node $HOSTURL to current cluster $OTHER"
        redis-cli --cluster add-node $HOSTURL $OTHER --cluster-slave
    fi

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


    HOSTNAME="$BASENAME-$(( $RANDOM % $MAX_NODE )).$BASENAME.$DOMAIN"
    HOSTURL="$(get_ip $HOSTNAME):6379"

    echo 
    echo "** Hostname:$HOSTNAME IP:$HOSTURL"

    redis-cli -c -h $HOSTNAME -p 6379 CLUSTER NODES
    redis-cli -c -h $HOSTNAME -p 6379 CLUSTER INFO

    remove_failed_nodes $HOSTNAME

    add_new_node $HOSTNAME 


    redis-cli --cluster check $HOSTURL
    redis-cli --cluster info  $HOSTURL

    sleep 60
done

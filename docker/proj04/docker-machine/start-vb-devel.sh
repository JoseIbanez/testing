#!/bin/sh

docker-machine rm kvstore

docker-machine create -d virtualbox kvstore

docker $(docker-machine config kvstore) run -d --net=host progrium/consul -server -bootstrap-expect 1
kvip=$(docker-machine ip kvstore)
echo $kvip

curl http://${kvip}:8500/v1/catalog/nodes
curl http://${kvip}:8500/v1/catalog/services
curl http://${kvip}:8500/v1/kv/docker/swarm/nodes

docker-machine rm swarm-master

docker-machine create \
        -d virtualbox \
        --engine-opt "cluster-store consul://${kvip}:8500" \
        --engine-opt "cluster-advertise eth1:2376" \
        --swarm \
        --swarm-master \
        --swarm-discovery consul://${kvip}:8500 \
        swarm-master


eval $(docker-machine env --swarm swarm-master)
docker info
docker ps -a



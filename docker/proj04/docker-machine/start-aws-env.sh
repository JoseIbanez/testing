#!/bin/sh


docker-machine create \
  --driver amazonec2 \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-request-spot-instance \
  --amazonec2-spot-price 0.10 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.large \
  kvstore


docker $(docker-machine config kvstore) \
  run -d --net=host progrium/consul -server -bootstrap-expect 1

##Error: Private IP!!
#kvip=$(docker-machine ip kvstore)
kvip=172.31.27.29
echo $kvip

curl http://${kvip}:8500/v1/catalog/nodes
curl http://${kvip}:8500/v1/catalog/services
curl http://${kvip}:8500/v1/kv/docker/swarm/nodes

docker-machine rm swarm-master

docker-machine create \
  --driver amazonec2 \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-request-spot-instance \
  --amazonec2-spot-price 0.10 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.large \
  --engine-opt "cluster-store consul://${kvip}:8500" \
  --engine-opt "cluster-advertise eth1:2376" \
  --swarm \
  --swarm-master \
  --swarm-discovery consul://${kvip}:8500 \
  swarm-master


eval $(docker-machine env --swarm swarm-master)
docker info
docker ps -a


docker-machine create \
  --driver amazonec2 \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-request-spot-instance \
  --amazonec2-spot-price 0.10 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.large \
  --engine-opt "cluster-store consul://${kvip}:8500" \
  --engine-opt "cluster-advertise eth1:2376" \
  --swarm \
  --swarm-discovery consul://${kvip}:8500 \
  swarm-agent-01 &

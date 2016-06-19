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
  run -d -p 8500:8500 progrium/consul -server -bootstrap-expect 1

##Error: Private IP!!
#kvip=$(docker-machine ip kvstore)
export kvip=`docker-machine inspect kvstore | jq -r '.Driver.PrivateIPAddress'`
#export kvip=172.31.21.206
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
  --engine-opt "cluster-advertise eth0:2376" \
  --swarm \
  --swarm-master \
  --swarm-discovery consul://${kvip}:8500 \
  swarm-master


eval $(docker-machine env --swarm swarm-master)
docker info
docker ps -a

docker network create -d overlay \
  --subnet=172.16.10.0/24 \
  --gateway=172.16.10.1 \
  my-net-01

docker network ls



docker-machine create \
  --driver amazonec2 \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-request-spot-instance \
  --amazonec2-spot-price 0.10 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.large \
  --engine-opt "cluster-store consul://${kvip}:8500" \
  --engine-opt "cluster-advertise eth0:2376" \
  --swarm \
  --swarm-discovery consul://${kvip}:8500 \
  swarm-agent-01 &

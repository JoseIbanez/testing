#!/bin/bash

#
# http://www.jillesvangurp.com/2016/08/26/running-consul-in-a-docker-swarm-with-docker-1-12/
#

docker network create -d overlay consul


docker service create \
  --name consul-cluster \
  --network consul \
  -p 8500:8500 \
  -e 'CONSUL_BIND_INTERFACE=eth0' \
  -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' \
  consul agent \
    -server -ui -client=0.0.0.0 \
    -bootstrap-expect=5 \
    -retry-join=consul-cluster \
    -retry-join=consul-cluster \
    -retry-join=consul-cluster \
    -retry-join=consul-cluster \
    -retry-join=consul-cluster

docker ps | grep consul-cluster  | cut -f 1 -d ' ' | xargs -n 1 -I {} docker exec {} consul members

docker service scale consul-cluster=3

docker ps | grep consul-cluster  | cut -f 1 -d ' ' | xargs -n 1 -I {} docker exec {} consul members

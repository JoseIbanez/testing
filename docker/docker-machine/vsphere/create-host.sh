#!/bin/bash

hcname=$1

kvip=$(docker-machine ip kvstore)
echo $kvip


docker-machine rm $hcname
docker-machine create \
--driver vmwarevsphere \
--vmwarevsphere-vcenter=192.168.1.50 \
--vmwarevsphere-username="root" \
--vmwarevsphere-password="vmware" \
--vmwarevsphere-datacenter="Homer" \
--vmwarevsphere-compute-ip="192.168.1.51" \
--vmwarevsphere-datastore="D0HP1" \
--vmwarevsphere-network="VM Network" \
        --engine-opt "cluster-store consul://${kvip}:8500" \
        --engine-opt "cluster-advertise eth1:2376" \
        --swarm \
        --swarm-discovery consul://${kvip}:8500 \
        $hcname



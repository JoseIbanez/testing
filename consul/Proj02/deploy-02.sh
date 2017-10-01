#!/bin/bash

#lxc profile create puppet-node
#lxc profile set puppet-node user.user-data - < ./config/my-cloud-config.yml
#lxc profile show puppet-node

lxc network create br0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
lxc network attach-profile br0 default


lxc launch ubuntu:16.04 u10 -p default
lxc launch ubuntu:16.04 u11 -p default

lxc exec u11 -- sh -c "wget http://google.es | gzip > 33.gz"

lxc launch images:centos/7/amd64   u20 -p default
lxc launch images:centos/6/amd64   u21 -p default

lxc list

lxc exec u20 bash
lxc exec u10 /bin/bash


for i in `seq 40 69`;
do
  sudo lxc launch ubuntu:14.04 u$i -p default
done

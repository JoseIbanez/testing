#!/bin/bash

lxc profile create puppet-node
lxc profile set puppet-node user.user-data - < ./config/my-cloud-config.yml
lxc profile show puppet-node

lxc launch ubuntu:14.04 u10 -p default -p puppet-node &
lxc launch ubuntu:14.04 u11 -p default -p puppet-node &


lxc exec u10 /bin/bash


for i in `seq 30 39`;
do
  lxc launch ubuntu:14.04 u$i -p default -p puppet-node &
done

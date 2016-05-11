#!/bin/bash

contName=$1

sudo lxc launch images:ubuntu/trusty/amd64 $contName

sudo lxc file push ./bin/consul $contName/usr/bin/
sudo lxc file push ./scripts/deploy-lxc.sh $contName/usr/local/

sudo lxc exec $1 /usr/local/deploy-lxc.sh 


#!/bin/bash

contName=$1

sudo lxc launch images:ubuntu/trusty/amd64 $contName

sudo lxc file push /vagrant/consul $contName/usr/bin/
sudo lxc file push /vagrant/deploy-lxc.sh $contName/usr/local/



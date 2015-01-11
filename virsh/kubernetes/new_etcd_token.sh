#!/bin/bash

rm ./etcd.token
wget https://discovery.etcd.io/new -O etcd.token

cat etcd.token
echo " "
echo " "



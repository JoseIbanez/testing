#!/bin/bash

# https://learn.hashicorp.com/tutorials/consul/deployment-guide

export http_proxy=http://192.168.1.20:8888
export https_proxy=http://192.168.1.20:8888


curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo \
    apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo \
    apt-get update -y
#sudo apt-get install consul=1.8.3
sudo \
    apt-get install -y consul

consul -v


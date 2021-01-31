#!/bin/bash

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install consul

cd ..
consul agent -dev -enable-script-checks -config-dir=./consul.d

dig @127.0.0.1 -p 8600 web.service.consul SRV
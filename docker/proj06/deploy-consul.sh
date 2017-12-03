#!/bin/bash
apt-get install -y curl unzip

mkdir -p /var/lib/consul
mkdir -p /usr/share/consul
mkdir -p /etc/consul/conf.d

curl -OL https://releases.hashicorp.com/consul/1.0.1/consul_1.0.1_linux_amd64.zip
unzip consul_1.0.1_linux_amd64.zip
mv consul /usr/local/bin/consul

curl -OL https://releases.hashicorp.com/consul/0.7.5/consul_1.0.1_web_ui.zip
unzip consul_1.0.1_web_ui.zip -d dist
mv dist /usr/share/consul/ui

cp consul-config/*.json /etc/consul/conf.d/

exit
consul agent -config-file /etc/consul/conf.d/bootstrap.json 

consul agent -config-file /etc/consul/conf.d/server.json 

consul members
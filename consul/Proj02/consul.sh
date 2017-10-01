#!/bin/sh

cd /tmp/

scp -r deploy@10.0.2.15:/vagrant/* .

sudo apt-get install -y unzip

#wget https://releases.hashicorp.com/consul/0.7.5/consul_0.7.5_linux_amd64.zip
wget https://releases.hashicorp.com/consul/0.9.3/consul_0.9.3_linux_amd64.zip
unzip -u consul*.zip
mv consul /usr/bin/consul

useradd consul

mkdir /etc/consul.d
mkdir -p /etc/consul.d/{bootstrap,server,client}

mkdir /var/consul
chown consul:consul /var/consul

consul --version

if bootstrap
cp ./config-consul/bootstrap.service /etc/systemd/system/consul.service
cp ./config-consul/bootstrap.json /etc/consul.d/bootstrap/

if server
cp ./config-consul/server.service /etc/systemd/system/consul.service
cp ./config-consul/server.json /etc/consul.d/server


systemctl start consul
systemctl status consul
journalctl --no-pager -u consul
consul members
#!/bin/bash

CONFIG=/etc/consul.d/server.hcl
sudo touch $CONFIG
sudo rm /etc/consul.d/consul.hcl 
sudo cp server.hcl $CONFIG
sudo chown --recursive consul:consul /etc/consul.d
sudo chmod 644 $CONFIG


SERVICE=/usr/lib/systemd/system/consul.service
sudo touch $SERVICE
sudo cp ./consul.service $SERVICE
sudo chown root:root $SERVICE
sudo chmod 644 $SERVICE


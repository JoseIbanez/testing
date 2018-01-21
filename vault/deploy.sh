#!/bin/bash

sudo apt-get install -y unzip
wget https://releases.hashicorp.com/vault/0.9.1/vault_0.9.1_linux_amd64.zip

unzip ./vault_0.9.1_linux_amd64.zip 
mv vault /usr/local/bin/
sudo mv vault /usr/local/bin/


sudo mkdir /etc/vault
sudo mkdir /var/lib/vault

sudo cp /vagrant/config-02.hcl /etc/vault/config.hcl

sudo vault server -config=/etc/vault/config.hcl 
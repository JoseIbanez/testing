#!/bin/bash

#For more info see: https://github.com/Juniper/ansible-junos-stdlib


declare -x http_proxy="http://10.74.42.22:8080"
declare -x https_proxy="https://10.74.42.22:8080"


apt-get install -y python-pip

pip install --upgrade pip

pip install ansible

pip install -r junos-requirements.txt

ansible-galaxy install Juniper.junos

mkdir /etc/ansible/
cp ../etc/ansible/hosts /etc/ansible/hosts 

mkdir /etc/ansible/facts.d/

sudo cp facts/* /etc/ansible/facts.d/
sudo chmod 666 /etc/ansible/facts.d/*


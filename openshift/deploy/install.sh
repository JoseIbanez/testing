#!/bin/bash

sudo yum install -y epel-release
sudo yum install -y python-pip

sudo umask 022 
sudo pip install --upgrade pip
sudo pip install ansible

###################################################################################
# Sandbox master key code
###################################################################################
mkdir -p ~/.secrets/
echo $sandboxKey > ~/.secrets/sandbox.key

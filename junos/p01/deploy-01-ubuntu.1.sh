#!/bin/sh

#==================================================
echo "Configure Additional Repo"

apt-get update -y

echo "Installing deps"
apt-get install -y \
  ntp \
  python-pip \
  python-dev \
  libxml2-dev \
  libxslt-dev \
  libssl-dev \
  libffi-dev 

#workarround for "cryptography" module
sudo pip install --upgrade setuptools
sudo apt-get install libffi-dev libssl-dev

#missing module enum
pip install enum34
pip install ipaddress

pip install awscli
pip install Jinja2
pip install junos-eznc

echo "Post configuration"
pip list | grep junos

#!/bin/sh

#==================================================
echo "Configure Additional Repo"

yum update -y

echo "Installing deps"

yum install -y \
  pip \
  python-devel \
  libxml2-devel \
  libxslt-devel \
  gcc \
  openssl \
  libffi-devel

#workarround for "cryptography" module
sudo pip install --upgrade setuptools
sudo apt-get install libffi-dev libssl-dev

#missing module enum
pip install enum34
pip install ipaddress

#pip as juniper web
pip install awscli
pip install Jinja2
pip install junos-eznc

echo "Post configuration"
pip list | grep junos

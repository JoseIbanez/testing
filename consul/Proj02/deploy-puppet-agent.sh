#!/bin/sh

curl -O https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb
sudo dpkg -i puppetlabs-release-pc1-xenial.deb
sudo apt-get -y update

sudo apt-get install -y puppet-agent

sudo systemctl start puppet
sudo systemctl enable puppet


#!/bin/bash

lxc profile create puppet-node
lxc profile set puppet-node user.user-data - < ./config/my-cloud-config.yml
lxc profile show puppet-node

lxc network attach-profile lxdbr0 default eth0


lxc launch ubuntu:14.04 u10 -p default -p puppet-node &
lxc launch ubuntu:14.04 u11 -p default -p puppet-node &

lxc launch images:centos/7/amd64   u20 -p default -p puppet-node
lxc launch images:centos/6/amd64   u30 -p default -p puppet-node


https://yum.puppetlabs.com/el/7/products/x86_64/puppet-3.8.7-1.el7.noarch.rpm

lxc exec u10 /bin/bash


for i in `seq 40 69`;
do
  sudo lxc launch ubuntu:14.04 u$i -p default -p puppet-node
done



yum install -y wget
yum install -y ruby
yum install -y "ruby(selinux)"
yum install -y dmidecode net-tools pciutils virt-what which
yum install -y augeas-libs

#Out of Centos:
wget https://yum.puppetlabs.com/el/7/products/x86_64/puppet-3.8.7-1.el7.noarch.rpm
wget https://yum.puppetlabs.com/el/7/products/x86_64/facter-2.4.6-1.el7.x86_64.rpm
wget https://yum.puppetlabs.com/el/7/products/x86_64/hiera-1.3.4-1.el7.noarch.rpm
wget https://yum.puppetlabs.com/el/7/dependencies/x86_64/ruby-augeas-0.4.1-3.el7.x86_64.rpm
wget https://yum.puppetlabs.com/el/7/dependencies/x86_64/ruby-rgen-0.6.5-2.el7.noarch.rpm
wget https://yum.puppetlabs.com/el/7/dependencies/x86_64/ruby-shadow-2.2.0-2.el7.x86_64.rpm





puppet apply /etc/puppet/manifests/projectname.pp

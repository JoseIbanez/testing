#!/bin/sh

curl -O https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb
sudo dpkg -i puppetlabs-release-pc1-xenial.deb
sudo apt-get update

sudo apt-get install -y puppetserver

sudo systemctl start puppetserver
sudo systemctl status puppetserver

exit

# maintenace commands
sudo /opt/puppetlabs/bin/puppet cert list
sudo /opt/puppetlabs/bin/puppet cert sign u10.lxd
sudo /opt/puppetlabs/bin/puppet cert sign --all


cd /vagrant 
cp puppet/init.pp /etc/puppetlabs/code/environments/production/manifests/site.pp


lxc exec u10 -- sh -c "/opt/puppetlabs/bin/puppet agent --test"
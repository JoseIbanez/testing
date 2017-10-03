#!/bin/sh

curl -O https://apt.puppetlabs.com/puppetlabs-release-pc1-xenial.deb
sudo dpkg -i puppetlabs-release-pc1-xenial.deb
sudo apt-get -y update

sudo apt-get install -y puppetserver

sudo systemctl start puppetserver
sudo systemctl enable puppetserver
sudo systemctl status puppetserver

/opt/puppetlabs/bin/puppet module install puppet-archive --version 2.0.0

exit

# maintenace commands
sudo /opt/puppetlabs/bin/puppet cert list
sudo /opt/puppetlabs/bin/puppet cert sign u10.lxd
sudo /opt/puppetlabs/bin/puppet cert sign --all


cd /vagrant 
MODULE_HOME=/etc/puppetlabs/code/environments/production/modules/
#cp puppet/init.pp /etc/puppetlabs/code/environments/production/manifests/site.pp
cp puppet/site.pp /etc/puppetlabs/code/environments/production/manifests/site.pp
cp -r puppet/modules/* $MODULE_HOME
tree $MODULE_HOME


lxc exec u11 -- sh -c "wget -qO- https://raw.githubusercontent.com/JoseIbanez/testing/master/consul/Proj02/deploy-puppet-agent.sh | sh"
lxc exec u11 -- sh -c "/opt/puppetlabs/bin/puppet agent --test"
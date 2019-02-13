#!/bin/bash

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
#sudo cp -a /vagrant/config/sources.list /etc/apt/sources.list
#dpkg --add-architecture i386


apt-get -y update && apt-get -y upgrade

echo "Installing pkgs"
sudo apt-get install puppetmaster-passenger


echo "Configuration"


echo "Restarting"
sudo service apache2 restart

echo "tools"

puppet cert list --all
puppet cert sign --all


puppet cert clean hostname


puppet config print | grep module
cd /etc/puppet/code
ln -s /vagrant/modules/ modules


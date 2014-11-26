#!/bin/sh 

hostname=$1

echo $hostname | sudo tee /etc/hostname 
grep $hostname /etc/hosts || echo "127.0.0.1   $hostname" | sudo tee -a /etc/hosts
sudo hostname -F /etc/hostname


wget -O - http://bootstrap.saltstack.org | sudo sh

sudo sed  's/^#master: salt/master: 10.19.30.150/g' -i /etc/salt/minion
sudo service salt-minion restart



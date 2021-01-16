#!/bin/sh
echo "Hello World!"
echo "This will run as soon as possible in the boot sequence"

#Apt
cat > /etc/apt/apt.conf.d/88apt-proxy << EOF
Acquire::http::Proxy "http://192.168.1.30:8000";
EOF
apt-get update
apt-get upgrade -y
apt-get install -y atop

#Hostname
hostname=`hostname`
#echo $hostname | sudo tee /etc/hostname 
grep $hostname /etc/hosts || echo "127.0.0.1   $hostname" | sudo tee -a /etc/hosts
#sudo hostname -F /etc/hostname

#Salt
#wget -O - http://bootstrap.saltstack.org | sudo sh
sudo apt-get install -y salt-minion
sudo sed  's/^#master: salt/master: 10.19.30.150/g' -i /etc/salt/minion
sudo service salt-minion restart


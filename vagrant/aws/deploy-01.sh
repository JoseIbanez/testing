#==================================
#Some configuration for S.O.
apt-get install joe
cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"

sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable 
sudo apt-get update -y

echo "Installing deps"
sudo apt-get install -y lxd
sudo lxd init --auto

echo "Post configuration"
#cp /vagrant/config/mongod.conf /etc/
cp -a /vagrant/scripts ./


echo "Restarting"
#sudo service mongod restart

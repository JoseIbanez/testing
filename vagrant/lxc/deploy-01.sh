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
sudo apt-get install -y unzip
sudo lxd init --auto


echo "Post configuration"
#cp /vagrant/config/mongod.conf /etc/
cp -a /vagrant/scripts ./

wget https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip
unzip ./consul_0.6.4_linux_amd64.zip
mkdir ./bin/
sudo mv consul ./bin/


echo "Restarting"
#sudo service mongod restart

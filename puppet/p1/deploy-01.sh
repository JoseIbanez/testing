apt-get install joe

cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
#sudo cp -a /vagrant/config/sources.list /etc/apt/sources.list
#dpkg --add-architecture i386

apt-get update -y

echo "Installing deps"
sudo apt-get install -y puppet

echo "Configuration"
#cp /vagrant/config/mongod.conf /etc/
#sudo ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4
cp -a /vagrant/manifests/ /etc/puppet/manifests
cp -a /vagrant/modules/   /etc/puppet/modules


echo "Restarting"
sudo service puppet stop

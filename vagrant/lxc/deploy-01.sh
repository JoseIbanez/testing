apt-get install joe

cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
#sudo cp -a /vagrant/config/sources.list /etc/apt/sources.list
#dpkg --add-architecture i386

sudo add-apt-repository ppa:ubuntu-lxc/lxd-stable 


sudo apt-get update -y

echo "Installing deps"
#sudo apt-get install -y lib32z1 lib32ncurses5 lib32bz2-1.0
#sudo apt-get install -y libssl1.0.0:i386
sudo apt-get install -y lxd

echo "Post configuration"
#cp /vagrant/config/mongod.conf /etc/
cp -a /vagrant/scripts ./


echo "Restarting"
#sudo service mongod restart

echo "Configure OS"
cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Mongodb repo"
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
apt-get update -y

echo "Installing Mongodb"
sudo apt-get install -y mongodb-org

echo "Post configuration"
cp /vagrant/config/mongod.conf /etc/

echo "Restarting"
sudo service mongod restart

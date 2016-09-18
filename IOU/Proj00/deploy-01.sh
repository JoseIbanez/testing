apt-get install joe

cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
sudo cp -a /vagrant/config/sources.list /etc/apt/sources.list
dpkg --add-architecture i386

apt-get update -y

echo "Installing deps"
sudo apt-get install -y lib32z1 lib32ncurses5 lib32bz2-1.0
sudo apt-get install -y libssl1.0.0:i386

echo "Post configuration"
#cp /vagrant/config/mongod.conf /etc/
sudo ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4


cp -a /vagrant/scripts ./


echo "Generate license file"
./scripts/keygen.py | grep -e 'lic' -e '=' > ~/.iourc


echo "Restarting"
#sudo service mongod restart

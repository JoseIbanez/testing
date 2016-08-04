#==================================
#Some configuration for S.O.
cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable
sudo apt-get update -y

echo "Installing deps"
#sudo apt-get install -y lxd


echo "Post configuration"
#sudo lxd init --auto


echo "Restarting"
#sudo service mongod restart
#https://insights.ubuntu.com/2016/04/07/lxd-networking-lxdbr0-explained/
#cp ./config/lxd-bridge /etc/default/lxd-bridge
#sudo service lxd-bridge stop && sudo service lxd restart



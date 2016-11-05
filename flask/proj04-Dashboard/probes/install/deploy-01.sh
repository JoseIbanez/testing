#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update


echo "Installing deps"
apt-get install -y \
        python-pip python-dev \
        libmysqlclient-dev

pip install flask flask-mysql




echo "Post configuration"


echo "Restarting"

#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update


echo "Installing deps"
apt-get install -y \
        git nano curl


echo "Post configuration"


echo "Restarting"


#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update

debconf-set-selections <<< 'mysql-server mysql-server/root_password password VFhcs123!'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password VFhcs123!'

echo "Installing deps"
apt-get install -y \
        mysql-server





echo "Post configuration"


echo "Restarting"


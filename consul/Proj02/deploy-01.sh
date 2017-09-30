#==================================
#Some configuration for S.O.
#cp /vagrant/config/locale /etc/default/locale


#==================================================
echo "Configure Additional Repo"
add-apt-repository -y ppa:ubuntu-lxc/lxd-stable
apt-get update -y

echo "Pre configuration"

echo "Installing deps"
apt-get install -y lxd \
                   lvm2 \
                   ansible

echo "Post configuration"
newgrp lxd
lxd init --auto



echo "Restarting"
service lxd restart

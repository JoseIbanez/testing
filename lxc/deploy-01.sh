#==================================
#Some configuration for S.O.
cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable
sudo apt-get update -y

echo "Installing deps"
sudo apt-get install -y lxd git lvm2


echo "Post configuration"
newgrp lxd
sudo lxd init --auto

mkdir Projects
cd Projects
git clone https://github.com/JoseIbanez/testing.git


sudo umount /mnt
sudo pvcreate /dev/xvdb
sudo pvcreate /dev/xvdc
sudo vgcreate vg0 /dev/xvdb /dev/xvdc
sudo lvcreate -L 78G -n lxc vg0
sudo mkfs.ext3 /dev/vg0/lxc


echo "Restarting"
#sudo service mongod restart
#https://insights.ubuntu.com/2016/04/07/lxd-networking-lxdbr0-explained/
cp ./config/lxd-bridge /etc/default/lxd-bridge
sudo service lxd-bridge stop
sudo service lxd stop

sudo mount /dev/vg0/lxc /var/lib/lxd/containers/
ls -l /var/lib/lxd/

sudo service lxd restart

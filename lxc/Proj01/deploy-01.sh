#==================================
#Some configuration for S.O.
cp /vagrant/config/locale /etc/default/locale

PASSWORD="Passw0rd"

#==================================================
echo "Configure Additional Repo"
add-apt-repository -y ppa:ubuntu-lxc/lxd-stable
apt-get update -y

echo "Pre configuration"
cp ./config/lxd-bridge /etc/default/lxd-bridge

echo "Installing deps"
apt-get install -y lxd lvm2

echo "Post configuration"
newgrp lxd
#lxd init --auto
lxd init --auto --network-address 0.0.0.0 --network-port 8443 --trust-password=$PASSWORD


sudo umount /mnt
sudo pvcreate /dev/xvdb
sudo pvcreate /dev/xvdc
sudo vgcreate vg0 /dev/xvdb /dev/xvdc
sudo lvcreate -L 78G -n lxc vg0
sudo mkfs.ext3 /dev/vg0/lxc


echo "Restarting"
service lxd stop

mount /dev/vg0/lxc /var/lib/lxd/containers/
ls -l /var/lib/lxd/

service lxd start

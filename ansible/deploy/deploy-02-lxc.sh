#==================================
#Some configuration for S.O.
#cp /vagrant/config/locale /etc/default/locale

PASSWORD="Passw0rd"

#==================================================
echo "Configure Additional Repo"

echo "Pre-configuration"

echo "Installing pkg"
apt install -t xenial-backports lxd lxd-client

echo "Post configuration"
#newgrp lxd
#lxd init --auto

#networking
lxd init --auto --network-address 0.0.0.0 --network-port 8443 --trust-password=$PASSWORD
lxc network create internal
lxc network attach-profile internal default eth0

#proxy for lxc images
lxc config set core.proxy_http  http://10.74.42.22:8080
lxc config set core.proxy_https https://10.74.42.22:8080
lxc config set core.proxy_ignore_hosts image-server.local

#storage
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

############################################
#create VMs...

lxc launch ubuntu:16.04 u10 -p default
lxc launch ubuntu:16.04 u11 -p default
lxc launch ubuntu:16.04 u12 -p default
lxc launch ubuntu:16.04 u13 -p default

lxc exec u11 -- sh -c "export http_proxy=http://10.74.42.22:8080 ; who ; apt-get install -y python"


lxc list

lxc exec u20 bash
lxc exec u10 /bin/bash



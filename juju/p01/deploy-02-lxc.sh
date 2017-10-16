#!/bin/bash

#==================================================
echo "Configure Additional Repo"
add-apt-repository --update -y ppa:ubuntu-lxc/lxd-stable

#==================================================
echo "Installing packages"
apt-get install -y lxd \
                   lvm2 \
                   thin-provisioning-tools \
                   tree \
                   ansible

#==================================================

echo "Post configuration"
newgrp lxd
lxd init --auto

echo "Restarting"
service lxd restart



lsblk

(
echo o # Create a new empty DOS partition table
echo n # Add a new partition
echo p # Primary partition
echo 1 # Partition number
echo   # First sector (Accept default: 1)
echo   # Last sector (Accept default: varies)
echo w # Write changes
) | sudo fdisk /dev/xvdh
lsblk

lxc storage create pool1 lvm source=/dev/xvdh1
vgdisplay
lxc profile device remove default root
lxc profile device add default root disk path=/ pool=pool1
lxc profile show default
lxc storage list
lxc storage volume list pool1


lxc network create br0 ipv6.address=none ipv4.address=10.0.3.1/24 ipv4.nat=true
lxc network attach-profile br0 default
lxc profile show default


lxc launch ubuntu:16.04 u10 -p default 
lxc launch ubuntu:16.04 u11 -p default
lxc launch ubuntu:16.04 u12 -p default
lxc launch ubuntu:16.04 u13 -p default
lxc launch ubuntu:16.04 u14 -p default






lxc exec u11 -- sh -c "wget http://google.es | gzip > 33.gz"

lxc launch images:centos/7/amd64   u20 -p default
lxc launch images:centos/6/amd64   u21 -p default

lxc list

lxc exec u20 bash
lxc exec u10 /bin/bash


for i in `seq 40 69`;
do
  sudo lxc launch ubuntu:14.04 u$i -p default
done

#!/bin/sh

#Usage: $0 <name> <master ip address>

name="$1"
master="$2"
image=/mnt/iso/img/coreos-beta.img

mkdir    /mnt/vm/$name
mkdir -p /mnt/vm/$name/configdrive/openstack/latest

cp $image  /mnt/vm/$name/d1.qcow2
#qemu-img create -f qcow2 /mnt/vm/$name/d2.qcow2 100G
#qemu-img create -f qcow2 /mnt/vm/$name/d3.qcow2 100G



cp cloud-config_node /tmp/cloud-config_$name 

sed -i "s/\$hostname/$name/"    /tmp/cloud-config_$name
sed -i "s/\$master/$master/"    /tmp/cloud-config_$name


#Ojo con permissos de apparmor
cp /tmp/cloud-config_$name /mnt/vm/$name/configdrive/openstack/latest/user_data



cat new_hs.xml | sed "s/hs00/$name/" > /tmp/new_$name.xml
virsh define /tmp/new_$name.xml
virsh start $name

#!/bin/sh


name="$1"
private_ipv4="$2"
public_ipv4="$2"
image=/mnt/iso/img/coreos-beta.img


mkdir    /mnt/vm/$name
mkdir -p /mnt/vm/$name/configdrive/openstack/latest

cp $image  /mnt/vm/$name/d1.qcow2
#qemu-img create -f qcow2 /mnt/vm/$name/d2.qcow2 100G
#qemu-img create -f qcow2 /mnt/vm/$name/d3.qcow2 100G



cp cloud-config /tmp/cloud-config_$name 

sed -i "s/hs00/$name/"                    /tmp/cloud-config_$name
sed -i "s/\$public_ipv4/$public_ipv4/"    /tmp/cloud-config_$name
sed -i "s/\$private_ipv4/$private_ipv4/"  /tmp/cloud-config_$name

cp /tmp/cloud-config_$name /mnt/vm/$name/configdrive/openstack/latest/user_data



cat new_hs.xml | sed "s/hs00/$name/" > /tmp/new_$name.xml
virsh define /tmp/new_$name.xml
virsh start $name

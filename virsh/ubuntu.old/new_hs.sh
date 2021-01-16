#!/bin/sh


name="$1"

mkdir /mnt/vm/$name

cp /mnt/iso/img/ubuntu_14.04_x64.qcow2  /mnt/vm/$name/d1.qcow2
qemu-img create -f qcow2 /mnt/vm/$name/d2.qcow2 100G
qemu-img create -f qcow2 /mnt/vm/$name/d3.qcow2 100G



cat cloud-config | sed "s/hs00/$name/" > /tmp/cloud-config_$name
write-mime-multipart   --output=/tmp/userdata_$name.txt \
   boot-script.sh:text/x-shellscript \
   /tmp/cloud-config_$name

cloud-localds /mnt/vm/$name/userdata.img /tmp/userdata_$name.txt


cat new_hs.xml | sed "s/hs00/$name/" > /tmp/new_$name.xml
virsh define /tmp/new_$name.xml
virsh start $name

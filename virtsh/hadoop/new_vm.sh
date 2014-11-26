#!/bin/sh


name="$1"

sudo mkdir /mnt/vm/$name

sudo cp /mnt/vm/img/ubuntu_12.04_x64.qcow2 /mnt/vm/$name/d1.qcow2
sudo qemu-img create -f qcow2 /mnt/vm/$name/d2.qcow2 100G



cat cloud-config | sed "s/s01/$name/" > /tmp/cloud-config_$name
write-mime-multipart   --output=/tmp/userdata_$name.txt \
   boot-script.sh:text/x-shellscript \
   /tmp/cloud-config_$name

sudo cloud-localds /mnt/vm/$name/userdata.img /tmp/userdata_$name.txt


cat new_s01.xml | sed "s/s01/$name/" > /tmp/new_$name.xml
sudo virsh define /tmp/new_$name.xml
sudo virsh start $name

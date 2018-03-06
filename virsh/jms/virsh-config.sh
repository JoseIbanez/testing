#!/bin/sh

sudo apt install -y qemu-kvm libvirt-bin
sudo apt-get install -y qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils

sudo adduser $USER libvirtd
sudo apt install virtinst




#https://www.cyberciti.biz/faq/linux-xen-vmware-kvm-intel-vt-amd-v-support/
dmesg | grep -i kvm

kvm-ok 
cat /sys/hypervisor/properties/capabilities



https://www.juniper.net/documentation/en_US/vsrx/topics/task/multi-task/security-vsrx-with-kvm-installing.html#jd0e230


cat /sys/module/kvm_intel/parameters/nested 

sudo rmmod kvm-intel
sudo sh -c "echo 'options kvm-intel nested=y enable_apicv=n pml=n' >> /etc/modprobe.d/dist.conf"
sudo modprobe kvm-intel


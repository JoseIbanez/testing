#!/bin/bash

VMNAME=u04
IP_ADDR=192.168.122.84


mkdir -p $HOME/kvm/$VMNAME
cd $HOME/kvm/$VMNAME

#Create root disk
qemu-img create -F qcow2 -b ~/kvm/base/focal-server-cloudimg-amd64.img -f qcow2 ./$VMNAME.qcow2 10G

INTERFACE=enp1s0

cat >network-config <<EOF
ethernets:
    $INTERFACE:
        addresses: 
        - $IP_ADDR/24
        dhcp4: false
        gateway4: 192.168.122.1
        nameservers:
            addresses: 
            - 1.1.1.1
            - 8.8.8.8
version: 2
EOF

cat >user-data <<EOF
#cloud-config
hostname: $VMNAME
manage_etc_hosts: true
users:
  - name: vmadm
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: users, admin
    home: /home/vmadm
    shell: /bin/bash
    lock_passwd: false
ssh_pwauth: true
disable_root: false
chpasswd:
  list: |
    vmadm:vmadm
  expire: false
EOF

touch meta-data

cloud-localds -v --network-config=network-config ./$VMNAME-seed.qcow2 user-data meta-data

virt-install --connect qemu:///system --virt-type kvm \
    --name $VMNAME \
    --ram 2048 --vcpus=2 \
    --os-type linux --os-variant ubuntu20.04 \
    --disk path=$HOME/kvm/$VMNAME/$VMNAME.qcow2,device=disk \
    --disk path=$HOME/kvm/$VMNAME/$VMNAME-seed.qcow2,device=disk \
    --import \
    --network network=default,model=virtio \
    --noautoconsole


#!/bin/bash

set -e


export RAM=4096
export CORES=2
export NETWORK=vlan-nodes
export DISK=40G


#Ubuntu 20.04
#export IMAGE=focal-server-cloudimg-amd64-disk-kvm.img

#Ubuntu 22.04
export IMAGE=jammy-server-cloudimg-amd64.img 

#More
#download from: https://cloud-images.ubuntu.com/focal/current/




create_vm() {

  sudo mkdir -p $HOME/kvm/$VMNAME
  sudo chown $USER:$USER $HOME/kvm/$VMNAME
  export VMHOME=$HOME/kvm/$VMNAME


  #Create root disk
  qemu-img create -F qcow2 -b ~/kvm/base/$IMAGE -f qcow2 $VMHOME/$VMNAME.qcow2 $DISK

  export INTERFACE=enp1s0

  cat >network-config <<EOF
ethernets:
    $INTERFACE:
        addresses: 
        - $IP_ADDR/24
        dhcp4: false
        gateway4: 10.39.122.1
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

  cloud-localds -v --network-config=network-config $VMHOME/$VMNAME-seed.qcow2 user-data meta-data

  virt-install --connect qemu:///system --virt-type kvm \
      --name $VMNAME \
      --ram $RAM --vcpus=$CORES \
      --os-variant ubuntu20.04 \
      --disk path=$VMHOME/$VMNAME.qcow2,device=disk \
      --disk path=$VMHOME/$VMNAME-seed.qcow2,device=disk \
      --import \
      --network network=$NETWORK,model=virtio \
      --noautoconsole

}


################# Create VMs

export VMNAME=nm01
export IP_ADDR=10.39.122.41
create_vm

export VMNAME=dn01
export IP_ADDR=10.39.122.42
create_vm

export VMNAME=dn02
export IP_ADDR=10.39.122.43
create_vm

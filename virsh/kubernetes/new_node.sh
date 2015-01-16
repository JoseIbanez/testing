#!/bin/sh


#Usage: $0 <name> <ip address>

hostname="$1"
image=/mnt/iso/img/coreos-beta.img
ram=2048
cores=2
private_ipv4="null"
public_ipv4="null"
discovery="null"





mkdir    /mnt/vm/$hostname
mkdir -p /mnt/vm/$hostname/configdrive/openstack/latest

cp $image  /mnt/vm/$hostname/d1.qcow2
#qemu-img create -f qcow2 /mnt/vm/$name/d2.qcow2 100G
#qemu-img create -f qcow2 /mnt/vm/$name/d3.qcow2 100G


# Prepare cloud-config file
file_cc="/tmp/cloud-config_$hostname"
cp cloud-config_node $file_cc 

sed -i "s/\$hostname/$hostname/"          $file_cc
sed -i "s/\$public_ipv4/$public_ipv4/"    $file_cc
sed -i "s/\$private_ipv4/$private_ipv4/"  $file_cc
sed -i "s@\$discovery@$discovery@"        $file_cc
sed -i "s@\$etcd_srv@$etcd_srv@"          $file_cc



#Ojo con permissos de apparmor
cp $file_cc /mnt/vm/$hostname/configdrive/openstack/latest/user_data


# Prepare kvm.xml file
file_xml="/tmp/kvm_$hostname"
cp kvm.xml $file_xml

sed -i "s/\$hostname/$hostname/"          $file_xml                         
sed -i "s/\$ram/$ram/"                    $file_xml                        
sed -i "s/\$cores/$cores/"                $file_xml

# Create virtual machine
virsh define $file_xml
virsh start $hostname

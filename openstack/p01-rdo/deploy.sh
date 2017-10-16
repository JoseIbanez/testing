yum 

wakeonlan 78:24:af:45:48:aa


sudo yum install -y net-tools

#static IP


# pre-requisite

sudo systemctl disable firewalld
sudo systemctl stop firewalld
sudo systemctl disable NetworkManager
sudo systemctl stop NetworkManager
sudo systemctl enable network
sudo systemctl start network

# test dns
ping homer.local

#/etc/enviroment

#openstack installation
sudo yum install -y centos-release-openstack-pike
yum-config-manager --enable openstack-pike
sudo yum update -y
sudo yum install -y openstack-packstack

#answer file
packstack --gen-answer-file=answer.txt
nano answer.txt 
packstack --answer-file=answer.txt


sudo packstack --allinone


# for centos and ubuntu, replace kvm by qemu in nova-compute.conf

#!/bin/sh

cd /tmp
sudo rm /tmp/hadoop*.tar*
wget http://ftp.grupofibratel.com/pub/Software/Cloud/Hadoop/hadoop-2.6.0.tar.gz

tar -xvz -f hadoop-*
sudo rm -rf /usr/local/hadoop/
sudo mv ./hadoop-2.6.0/ /usr/local/hadoop/

cp /home/ubuntu/*-site.xml /usr/local/hadoop/etc/hadoop/

sudo chown -R hduser:hadoop /usr/local/hadoop

mkdir /mnt/hadoop/s1/namenode
mkdir /mnt/hadoop/s1/datanode

sudo chown -R hduser:hadoop /mnt/hadoop

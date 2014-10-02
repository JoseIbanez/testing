#!/bin/sh


cd /tmp
wget http://ftp.grupofibratel.com/tmp/hadoop/hbase-0.98.6.1-hadoop2-bin.tar.gz

tar -xzv -f ./hbase-0.98.6.1-hadoop2-bin.tar.gz
sudo mv hbase-0.98.6.1-hadoop2 /usr/local/hbase

sudo mkdir /usr/local/zookeeper

sudo chown -R hduser: /usr/local/hbase      
sudo chown -R hduser: /usr/local/zookeeper


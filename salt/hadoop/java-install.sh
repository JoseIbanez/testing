#!/bin/sh

cd /tmp
wget http://ftp.grupofibratel.com/pub/Software/Cloud/Hadoop/jdk-7u76-linux-i586.tar.gz
tar -xvz -f jdk-7*

sudo mkdir /usr/local/java
sudo mv ./jdk1.7* /usr/local/java/jdk1.7.0

sudo update-alternatives --install "/usr/bin/java"   "java"   "/usr/local/java/jdk1.7.0/bin/java"   1
sudo update-alternatives --install "/usr/bin/javac"  "javac"  "/usr/local/java/jdk1.7.0/bin/javac"  1 
sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/local/java/jdk1.7.0/bin/javaws" 1
sudo update-alternatives --install "/usr/bin/jps"    "jps"    "/usr/local/java/jdk1.7.0/bin/jps"    1


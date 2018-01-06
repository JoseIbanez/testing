#!/bin/sh

#Pre-requisites
apt-get update -y
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

#Key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88

#New repo
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

#Instalation
apt-get update -y
apt-get install -y docker-ce

#Test
docker run hello-world


groupadd docker
usermod -aG docker $USER
usermod -aG docker ubuntu


systemctl enable docker


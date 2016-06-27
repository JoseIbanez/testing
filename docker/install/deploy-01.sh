#!/bin/sh

apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
add-apt-repository "deb https://apt.dockerproject.org/repo ubuntu-wily main"

apt-get update -y
apt-cache policy docker-engine

apt-get install docker-engine
service docker start
#!/bin/bash


yum install -y rpm-build wget tree

wget https://github.com/opensourceway/how-to-rpm/raw/master/utils.tar



mkdir -p ./rpmbuild/RPMS/noarch
mkdir -p ./rpmbuild/SOURCES/
mkdir -p ./rpmbuild/SPECS/
mkdir -p ./rpmbuild/SRPMS

ln -s $PWD/development/spec/utils.spec ./rpmbuild/SPECS/

rpmbuild --target noarch -bb utils.spec

sudo rpm -q  --changelog utils

sudo rpm -ivh /home/vagrant/rpmbuild/RPMS/noarch/utils-1.0.0-1.noarch.rpm
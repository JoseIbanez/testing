#!/bin/sh

sudo apt-get -y purge  vagrant
wget https://releases.hashicorp.com/vagrant/1.8.5/vagrant_1.8.5_x86_64.deb
sudo dpkg -i ./vagrant_1.8.5_x86_64.deb


vagrant plugin install vagrant-aws
vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box


export AWS_ACCESS_KEY_ID=`cat  ~/.aws/credentials | grep aws_access_key_id | cut -d ' ' -f 3`
export AWS_SECRET_ACCESS_KEY=`cat  ~/.aws/credentials | grep aws_secret | cut -d ' ' -f 3`



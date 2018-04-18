#!/bin/bash

# npm
apt-get update -y
apt-get install -y nodejs npm


# Mongo-DB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update -y
apt-get install -y mongodb-org



### npm enviroment
# for Vagrant WIN: use --no-bin-links

npm install --no-bin-links --save-dev nodemon
npm install --no-bin-links express --save
npm install mongoose --save


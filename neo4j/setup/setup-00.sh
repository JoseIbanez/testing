#!/bin/bash

sudo apt-get update 

# Docker.io
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
sudo usermod -aG docker vagrant

# Docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

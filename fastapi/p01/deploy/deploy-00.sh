#!/bin/bash

#exit on first error
set -e


#Ubuntu setup
sudo apt-get update
sudo apt-get install -y docker.io
sudo apt-get install -y python3-venv python3-dev

sudo usermod -aG docker $USER



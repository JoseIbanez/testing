#!/bin/bash

#exit on first error
set -e


#Ubuntu 18.04 setup
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev
python3 -m venv $HOME/py-venv3
source $HOME/py-venv3/bin/activate

pip install --upgrade pip 
pip install --upgrade setuptools wheel twine
pip install --upgrade --ignore-installed PyYAML


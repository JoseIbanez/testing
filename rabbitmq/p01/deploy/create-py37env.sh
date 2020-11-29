#!/bin/bash


sudo apt-get install -y python3.7-venv python3.7-dev


python3.7 -m venv $HOME/py-venv37
source $HOME/py-venv37/bin/activate

pip install --upgrade pip 
pip install --upgrade setuptools wheel twine
pip install --upgrade --ignore-installed PyYAML


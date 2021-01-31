#!/bin/bash

python3 -m venv $HOME/py-venv36
source $HOME/py-venv36/bin/activate

pip install --upgrade pip 
pip install --upgrade setuptools wheel twine
pip install --upgrade --ignore-installed PyYAML


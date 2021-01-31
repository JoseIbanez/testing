#!/bin/bash


sudo apt-get install -y python3.7-venv python3.7-dev libpq-dev

#sudo apt-get install -y --no-install-recommends \
#     build-essential libssl-dev libffi-dev \
#     libxml2-dev libxslt1-dev zlib1g-dev 

python3.7 -m venv $HOME/py-venv37
source $HOME/py-venv37/bin/activate
ls $HOME

pip install --upgrade pip 
pip install --upgrade setuptools wheel twine
pip install --upgrade --ignore-installed PyYAML

pip install -r requirements.txt


#postgres
#pip install psycopg2
#pip install psycopg2-binary
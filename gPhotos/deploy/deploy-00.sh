#!bin/bash

sudo apt-get -y update
sudo apt-get install -y screen nano
sudo apt-get install -y python3-venv python3-dev
sudo apt-get install -y build-essential

python3 -V
python3 -m venv ~/py36-venv


pwd
echo $HOME
source ~/py36-venv/bin/activate


pip install gphotospy

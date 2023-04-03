#!/bin/bash

export SERVICE_NAME=acelinkd

sudo service $SERVICE_NAME stop || echo ""

sudo rm -rf /usr/local/bin/$SERVICE_NAME/
sudo mkdir -p /usr/local/bin/$SERVICE_NAME/
sudo chown $USER /usr/local/bin/$SERVICE_NAME

deactive || echo ""
python3.10 -m venv /usr/local/bin/$SERVICE_NAME/venv
source /usr/local/bin/$SERVICE_NAME/venv/bin/activate
pip install ..

envsubst < ./$SERVICE_NAME.service  | sudo tee /etc/systemd/system/$SERVICE_NAME.service

sudo systemctl enable $SERVICE_NAME
sudo systemctl stop $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME
sudo journalctl -u $SERVICE_NAME



#!/bin/bash

#server
sudo apt-get install -y --no-install-recommends python-minimal python-pip gunicorn
sudo pip install redis Flask

#client

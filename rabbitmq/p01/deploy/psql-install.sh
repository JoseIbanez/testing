#!/bin/bash

sudo apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common



sudo -u postgres createuser -D -w demo
sudo -u postgres createuser -D -w user1
sudo -u postgres createuser -D -w flask

sudo -u postgres createdb vc_deployments


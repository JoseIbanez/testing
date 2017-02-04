#!/bin/bash
op=`pwd`

cd $op/../../db/install
source ./mysql.env
./deploy-01.sh

cd $op/../../rproxy/dev
./deploy-01.sh

apt-get update && apt-get install -y \
          build-essential screen \
          python-pip python-dev \
          gunicorn \
          libmysqlclient-dev

pip install \
          flask \
          flask-mysql

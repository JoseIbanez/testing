#!/bin/sh
#Install script

cp uwsgi.service /etc/systemd/system/uwsgi.service
systemctl daemon-reload


rm /etc/nginx/sites-enabled/default
cp ./nginx_proj01 /etc/nginx/sites-enabled/default




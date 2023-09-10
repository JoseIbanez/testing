#!/bin/bash

sudo apt-get install nginx
cp r-hls /etc/nginx/sites-enabled/
cp cache.conf /etc/nginx/conf.d/
mkdir -p /var/lib/nginx/cache

service nginx restart

systemctl status nginx
journalctl -u nginx
journalctl -xe

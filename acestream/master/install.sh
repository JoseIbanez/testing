#!/bin/bash

sudo apt-get install nginx
cp nginx-hls /etc/nginx/sites-enabled/hls


mkdir -p /mnt/d1/hls/error/
cp error-page/custom_404.html /mnt/d1/hls/error/


service nginx restart

systemctl status nginx
journalctl -u nginx
journalctl -xe



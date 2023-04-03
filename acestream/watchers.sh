#!/bin/bash

tail -n 100 /var/log/nginx/access.log | grep m3u8 | cut -d'"' -f 6 | sort | uniq -c



#!/bin/bash

tail -n 100 /var/log/nginx/access.log | cut -d'"' -f 6 | sort -u



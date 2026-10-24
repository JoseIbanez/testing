#!/bin/bash

#Use normal user, no root
useradd -u 1000 acelink

/usr/bin/supervisord

runuser -u acelink /acelink/internal-hls.sh



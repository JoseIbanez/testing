#!/bin/bash

home="/home/pi/Projects/rp-iot/p04-twitter"

cd $home

file=`ls -1 /media/pic/*.jpg | tail -n 1`

./upload.01.py -f $file -t $file

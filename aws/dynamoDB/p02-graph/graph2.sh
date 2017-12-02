#!/bin/bash

home="/home/ubuntu/Projects/testing/aws/dynamoDB/p02-graph"
cd $home

./get_temp.py -probe b827eb.300520.c3 -today -hours 48 > ./sample.csv

gnuplot ./g1.plot
./tw_upload.py -f temp.png -t "19250 Temperature"

gnuplot ./humidity.plot
./tw_upload.py -f humidity.png -t "19250 Humidity"


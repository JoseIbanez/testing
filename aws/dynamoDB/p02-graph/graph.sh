#!/bin/bash

home="/home/ubuntu/Projects/testing/aws/dynamoDB/p02-graph"
cd $home

./get_temp.py -probe b827eb.300520.c2 > ./sample.csv
gnuplot ./g1.plot
./tw_upload.py -f temp.png -t 28039

./get_temp.py -probe b827eb.61eb84.c3  > ./sample.csv
gnuplot ./g1.plot
./tw_upload.py -f temp.png -t 19250 


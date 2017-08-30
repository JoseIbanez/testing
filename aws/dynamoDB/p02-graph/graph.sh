#!/bin/bash

./get_temp.py > ./sample.csv
gnuplot ./g1.plot
./tw_upload.py -f temp.png -t 4C
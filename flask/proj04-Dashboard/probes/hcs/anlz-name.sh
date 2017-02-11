#!/bin/bash

tar=$1
file=$2

tar -xzO -f $tar $file | ./anlz-tar.py -n $file  --debug

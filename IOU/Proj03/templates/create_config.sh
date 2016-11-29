#!/bin/bash

group=$1
config=$2
template=$3

if [ "$group" = "sw" ]; then
  devices="s11 s12 s21 s22"
elif [ "$group" = "fw" ]; then
  devices="a13 a23"
elif [ "$group" = "pe" ]; then
  devices="p19 p29"
elif [ "$group" = "all" ]; then
  devices="s11 s12 s21 s22 a13 a23 p19 p29"
fi

set -f                      # avoid globbing (expansion of *).
array=(${devices// / })
for dev in "${array[@]}"
do
    echo "$dev"
    cat ${config}.yaml | sed "s/#Device$dev//g" | grep -v "#Device" | grep -v "^$" > ../cmd/${config}.${dev}.yaml
    ./render.py -c ../cmd/${config}.${dev}.yaml -t ${template}.nj2 > ../cmd/${template}.${dev}.cmd

done



#./render.py -c ${config}.aa.yaml -t ${template}.nj2 > ../cmd/${template}.s11.cmd

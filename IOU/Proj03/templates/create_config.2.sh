#!/bin/bash

group=$1
config=$2
template=$3


cat ${config}.yaml | grep -v "#DCB" | grep -v "#DeviceB" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.aa.yaml
cat ${config}.yaml | grep -v "#DCB" | grep -v "#DeviceA" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.ab.yaml
cat ${config}.yaml | grep -v "#DCA" | grep -v "#DeviceB" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.ba.yaml
cat ${config}.yaml | grep -v "#DCA" | grep -v "#DeviceA" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.bb.yaml
cat ${config}.yaml | grep -v "#DCB" | grep -v "#Device"  | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.a.yaml
cat ${config}.yaml | grep -v "#DCA" | grep -v "#Device"  | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ../cmd/${config}.b.yaml


if [ "$group" = "sw" ]; then
  ./render.py -c ../cmd/${config}.aa.yaml -t ${template}.nj2 > ../cmd/${template}.s11.cmd
  ./render.py -c ../cmd/${config}.ab.yaml -t ${template}.nj2 > ../cmd/${template}.s12.cmd
  ./render.py -c ../cmd/${config}.ba.yaml -t ${template}.nj2 > ../cmd/${template}.s21.cmd
  ./render.py -c ../cmd/${config}.bb.yaml -t ${template}.nj2 > ../cmd/${template}.s22.cmd
elif [ "$group" = "fw" ]; then
  ./render.py -c ../cmd/${config}.a.yaml -t ${template}.nj2 > ../cmd/${template}.a13.cmd
  ./render.py -c ../cmd/${config}.b.yaml -t ${template}.nj2 > ../cmd/${template}.a23.cmd
elif [ "$group" = "pe" ]; then
  ./render.py -c ../cmd/${config}.a.yaml -t ${template}.nj2 > ../cmd/${template}.p19.cmd
  ./render.py -c ../cmd/${config}.b.yaml -t ${template}.nj2 > ../cmd/${template}.p29.cmd
fi

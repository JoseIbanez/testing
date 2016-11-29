#!/bin/bash

config=$1
template=$2


cat ${config}.yaml | grep -v "#DCB" | grep -v "#DeviceB" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ${config}.aa.yaml
cat ${config}.yaml | grep -v "#DCB" | grep -v "#DeviceA" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ${config}.ab.yaml
cat ${config}.yaml | grep -v "#DCA" | grep -v "#DeviceB" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ${config}.ba.yaml
cat ${config}.yaml | grep -v "#DCA" | grep -v "#DeviceA" | sed 's/#[A-Za-z]\+//g'  | grep -v "^$" > ${config}.bb.yaml


./render.py -c ${config}.aa.yaml -t ${template}.nj2 > ../cmd/${template}.s11.cmd
./render.py -c ${config}.ab.yaml -t ${template}.nj2 > ../cmd/${template}.s12.cmd
./render.py -c ${config}.ba.yaml -t ${template}.nj2 > ../cmd/${template}.s21.cmd
./render.py -c ${config}.bb.yaml -t ${template}.nj2 > ../cmd/${template}.s22.cmd

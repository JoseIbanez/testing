#!/bin/bash

group=$1
config=$2

export lote_name=$config
export lote_date=`date +%s`

if [ "$group" = "sw" ]; then
 ./ios_cmd.v3.exp Cust00 localhost 2011 s11 ../secret/dummy.scrt ../cmd/${config}.s11.cmd
 ./ios_cmd.v3.exp Cust00 localhost 2012 s12 ../secret/dummy.scrt ../cmd/${config}.s12.cmd
 ./ios_cmd.v3.exp Cust00 localhost 2021 s21 ../secret/dummy.scrt ../cmd/${config}.s21.cmd
 ./ios_cmd.v3.exp Cust00 localhost 2022 s22 ../secret/dummy.scrt ../cmd/${config}.s22.cmd
fi

if [ "$group" = "fw" ]; then
 ./ios_cmd.v3.exp Cust00 localhost 2013 s13 ../secret/dummy.scrt ../cmd/${config}.a13.cmd
 ./ios_cmd.v3.exp Cust00 localhost 2023 s23 ../secret/dummy.scrt ../cmd/${config}.a23.cmd
fi

if [ "$group" = "pe" ]; then
../expect/ios_cmd.v3.exp Cust00 localhost 2011 pe11 ../secret/dummy.scrt ../cmd/${config}.pe11.cmd
../expect/ios_cmd.v3.exp Cust00 localhost 2012 pe12 ../secret/dummy.scrt ../cmd/${config}.pe12.cmd
../expect/ios_cmd.v3.exp Cust00 localhost 2013 pe13 ../secret/dummy.scrt ../cmd/${config}.pe13.cmd
../expect/ios_cmd.v3.exp Cust00 localhost 2014 pe14 ../secret/dummy.scrt ../cmd/${config}.pe14.cmd
../expect/ios_cmd.v3.exp Cust00 localhost 2015 pe15 ../secret/dummy.scrt ../cmd/${config}.pe15.cmd
fi

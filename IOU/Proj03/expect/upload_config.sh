#!/bin/bash

config=$1
perhost=$2

export lote_name=$config
export lote_date=`date +%s`


./ios_cmd.v3.exp Cust00 localhost 2011 s11 ../secret/dummy.scrt ../cmd/${config}.s11.cmd
./ios_cmd.v3.exp Cust00 localhost 2012 s12 ../secret/dummy.scrt ../cmd/${config}.s12.cmd
./ios_cmd.v3.exp Cust00 localhost 2021 s21 ../secret/dummy.scrt ../cmd/${config}.s21.cmd
./ios_cmd.v3.exp Cust00 localhost 2022 s22 ../secret/dummy.scrt ../cmd/${config}.s22.cmd

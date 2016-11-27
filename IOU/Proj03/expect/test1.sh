#!/bin/bash

export lote_name="Test"
export lote_date=`date +%s`

./ios_cmd.v3.exp Cust00 localhost 2001 m1 ../secret/dummy.scrt ../cmd/cmd0.cmd


./ios_cmd.v3.exp Cust00 localhost 2011 s11 ../secret/dummy.scrt ../cmd/cmd1.cmd
./ios_cmd.v3.exp Cust00 localhost 2012 s12 ../secret/dummy.scrt ../cmd/cmd1.cmd
./ios_cmd.v3.exp Cust00 localhost 2021 s21 ../secret/dummy.scrt ../cmd/cmd1.cmd
./ios_cmd.v3.exp Cust00 localhost 2022 s22 ../secret/dummy.scrt ../cmd/cmd1.cmd

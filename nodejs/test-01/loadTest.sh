#!/bin/bash

timeStart=`date`

COUNTER=0
while [  $COUNTER -lt 500 ]; do

    wget -qO-  http://127.0.0.1/?number=103

     let COUNTER=COUNTER+1 
done


echo $timeStart
date

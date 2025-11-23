#!/bin/bash


datafile="/mnt/d2/esdumps/meraki-o-$1.jsonl"

echo $datafile
if [ -f "$datafile.gz" ] 
then mv "$datafile.gz" "$datafile.gz.$(date +%H%M%S)"
fi


gzip "$datafile"

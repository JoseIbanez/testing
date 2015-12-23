#!/bin/sh

url="http://52.29.53.80"

while [ 1 ]
do
  wget -c $url
  sleep 1
done

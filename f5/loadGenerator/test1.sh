#!/bin/bash


for i in {1..5000}
do
   echo "Welcome $i times"
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   curl http://3.0.0.1 &
   sleep 1
done

#!/bin/bash

IOU="/home/ubuntu/IOU"

for n in {1..5}
do
echo $n
port=$((2000 + $n))
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p $port -- -e2 -s0 $n &
sleep 5
done


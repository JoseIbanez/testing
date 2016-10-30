#!/bin/sh

if [ -z $1 ]
then
   size="m4.large";
else
   size=$1
fi


if [ -z $2 ]
then
   price="0.05"
else
   price=$2
fi


cat ./myVM.j2 | sed  "s/{{size}}/$size/g" > /tmp/myVM.json

cat /tmp/myVM.json

aws ec2 \
request-spot-instances \
--spot-price "$price" \
--instance-count 1 \
--type "one-time" \
--launch-specification file:///tmp/myVm.json

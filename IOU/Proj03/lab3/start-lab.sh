#!/bin/sh

group=$1

IOU="/opt/IOU"
#IMG0="i86bi-linux-l2-adventerprisek9-15.6.0.9S.bin"
IMG0="i86bi-linux-l2-adventerprisek9-15.2d.bin"
IMG1="i86bi-linux-l3-ipbase-12.4.bin"
IMG2=""

#Download missing images
for IMG in $IMG0 $IMG1  ; do
  echo $IMG

  if [ ! -f $IOU/bin/$IMG ]; then
     sudo aws --region eu-west-1 s3 cp \
        s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4/bin/$IMG \
        $IOU/bin/
     sudo chmod +x $IOU/bin/*
  fi

done


#SW
if [ "$group" = "sw" ]; then
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG0 -p 2071 -- -e2 -s0 71 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG0 -p 2072 -- -e2 -s0 72 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG0 -p 2091 -- -e2 -s0 91 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG0 -p 2092 -- -e2 -s0 92 &
fi

#HOST
if [ "$group" = "host" ]; then
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG1 -p 2007 -- -e1 -s0 7 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IOU/bin/$IMG1 -p 2009 -- -e1 -s0 9 &
fi


if  [ "$group" = "stop" ]; then
  killall /opt/IOU/scripts/wrapper.bin
  ps -xau | grep wrapper
fi
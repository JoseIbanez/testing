#!/bin/sh

group=$1

IOU="/opt/IOU"
IMG0=$IOU/bin/i86bi-linux-l3-ipbase-12.4.bin
IMG1=$IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin
IMG2=$IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin



#External Network
if [ "$group" = "ext" ]; then
  sleep 2; $IOU/scripts/wrapper.bin -m $IMG0 -p 2001 -- -e1 -s0 01 &
  sleep 5; sudo $IOU/scripts/iou2net.pl -t tap0 -p 50 &
fi

#CORE
if [ "$group" = "core" ]; then
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG2 -p 2021 -- -e2 -s0 21 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG2 -p 2022 -- -e2 -s0 22 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG2 -p 2023 -- -e2 -s0 23 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG2 -p 2024 -- -e2 -s0 24 &
fi

#MPLS
if [ "$group" = "core" ]; then
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG1 -p 2011 -- -e2 -s0 11 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG1 -p 2012 -- -e2 -s0 12 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG1 -p 2013 -- -e2 -s0 13 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG1 -p 2014 -- -e2 -s0 14 &
   sleep 2; $IOU/scripts/wrapper.bin -m $IMG1 -p 2015 -- -e2 -s0 15 &
fi

#!/bin/sh

IOU="/opt/IOU"
IMG0=$IOU/bin/i86bi-linux-l3-ipbase-12.4.bin

IMG1=$IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin
IMG2=$IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin


#MPLS
sleep 5; $IOU/scripts/wrapper.bin -m $IMG1 -p 2011 -- -e2 -s0 11 &
sleep 5; $IOU/scripts/wrapper.bin -m $IMG1 -p 2012 -- -e2 -s0 12 &
sleep 5; $IOU/scripts/wrapper.bin -m $IMG1 -p 2013 -- -e2 -s0 13 &
sleep 5; $IOU/scripts/wrapper.bin -m $IMG1 -p 2014 -- -e2 -s0 14 &
sleep 5; $IOU/scripts/wrapper.bin -m $IMG1 -p 2015 -- -e2 -s0 15 &




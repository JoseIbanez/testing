#!/bin/sh

IOU="/opt/IOU"

$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-ipbase-12.4.bin -p 2001 -- -e4 -s0 01 &
sleep 5


$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin -p 2011 -- -e4 -s0 11 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin -p 2012 -- -e4 -s0 12 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin -p 2021 -- -e4 -s0 21 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l2-ipbasek9-15.1g.bin -p 2022 -- -e4 -s0 22 &
sleep 5


$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin -p 2013 -- -e4 -s0 13 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin -p 2023 -- -e4 -s0 23 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin -p 2019 -- -e4 -s0 19 &
sleep 5
$IOU/scripts/wrapper.bin -m $IOU/bin/i86bi-linux-l3-adventerprisek9-12.4.bin -p 2029 -- -e4 -s0 29 &
sleep 5


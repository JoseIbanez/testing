#!/bin/sh
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2031 -- -e2 -s0 31 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2032 -- -e2 -s0 32 &
sleep 5


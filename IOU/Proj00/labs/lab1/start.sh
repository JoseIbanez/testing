#!/bin/sh
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2001 -- -e2 -s0 1 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2002 -- -e2 -s0 2 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2003 -- -e2 -s0 3 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2004 -- -e2 -s0 4 &
sleep 5


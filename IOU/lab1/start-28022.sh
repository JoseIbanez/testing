#!/bin/sh
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2011 -- -e2 -s0 11 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2012 -- -e2 -s0 12 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2013 -- -e2 -s0 13 &
sleep 5
../../scripts/wrapper.bin -m /vagrant/Cisco-IOU-L2-L3-Collection-v4/bin/i86bi-linux-l3-adventerprisek9-15.4.1T.bin -p 2014 -- -e2 -s0 14 &
sleep 5


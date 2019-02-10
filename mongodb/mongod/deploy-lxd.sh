#!/bin/bash

adduser vagrant lxd
newgrp lxd
id

cat lxd.yaml | lxd init --preseed

lxc launch ubuntu:18.04 u01
lxc launch ubuntu:18.04 u02
lxc launch ubuntu:18.04 u10 
lxc launch ubuntu:18.04 u20 


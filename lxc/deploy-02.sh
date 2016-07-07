#!/bin/bash

lxc profile create puppet-node
lxc profile set puppet-node user.user-data - < my-cloud-config.yml


lxc launch ubuntu:14.04 u10 -p default -p puppet-node &
lxc launch ubuntu:14.04 u11 -p default -p puppet-node &


lxc exec u10 /bin/bash

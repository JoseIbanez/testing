#!/bin/bash

IPADDR=$(ip a show enp0s8 | grep "inet " | awk '{print $2}' | cut -d / -f1)
IIFACE="enp0s8"

export INSTALL_K3S_EXEC="  --flannel-iface=${IIFACE} --node-ip=${IPADDR}" 
export K3S_URL=https://172.28.128.3:6443 
export K3S_TOKEN="K100b9e88cad425ff134449ef525e8edc7189980007827559d1752844b69cacaeeb::node:4561fdc639dc878ddc00bc010e50e0e6"

curl -sfL https://get.k3s.io |  sh -

ip -d l show flannel.1


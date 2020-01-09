#!/bin/bash

IPADDR=$(ip a show enp0s8 | grep "inet " | awk '{print $2}' | cut -d / -f1)
IIFACE="enp0s8"

export INSTALL_K3S_EXEC="  --flannel-iface=${IIFACE} --node-ip=${IPADDR}" 
export K3S_URL=https://172.28.128.5:6443 
export K3S_TOKEN="K10b1097610943a5dfeb54e0abc3f8e4736edad1c1359c27e8b143f8d08dd9d6c5b::server:cd652ec85f2e0457c982ce8db018f816"

curl -sfL https://get.k3s.io |  sh -

ip -d l show flannel.1


#!/bin/bash

IPADDR=$(ip a show enp0s8 | grep "inet " | awk '{print $2}' | cut -d / -f1)
IIFACE="enp0s8"
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="  --flannel-iface=${IIFACE} --node-ip=${IPADDR}" sh -

ip -d l show flannel.1
cat /var/lib/rancher/k3s/server/node-token
cat /etc/rancher/k3s/k3s.yaml

sudo kubectl get node


#!/bin/sh

cd /etc/swift

scp -i /home/fibratel/.ssh/swf_id_rsa  \
    -o "StrictHostKeyChecking no" \
    fibratel@10.19.11.160:/etc/swift/*.ring.gz .

chown -R swift:swift /etc/swift

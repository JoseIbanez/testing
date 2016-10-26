#!/bin/sh
node=$1

mkdir -p /mnt/tmp/lo1
mkfs.msdos -C $node.img 1440
sudo mount -o loop ./$node.img /mnt/tmp/lo1
sudo cp $node.cfg /mnt/tmp/lo1/ks.cfg
sleep 1
sudo umount /mnt/tmp/lo1

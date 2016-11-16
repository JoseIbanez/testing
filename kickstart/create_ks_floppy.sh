#!/bin/sh
node=$1
ip=$2
mask=$3
gw=$4

cp ./tropo-00.cfg $node.cfg

sed -i "s/{{ip}}/$ip/g" $node.cfg
sed -i "s/{{gw}}/$gw/g" $node.cfg
sed -i "s/{{mask}}/$mask/g" $node.cfg
sed -i "s/{{hostname}}/$node/g" $node.cfg



mkdir -p /mnt/tmp/lo1
mkfs.msdos -C $node.img 1440
sudo mount -o loop ./$node.img /mnt/tmp/lo1
sudo cp $node.cfg /mnt/tmp/lo1/ks.cfg
sleep 1
sudo umount /mnt/tmp/lo1

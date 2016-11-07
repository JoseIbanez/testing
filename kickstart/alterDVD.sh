#!/bin/sh

mkdir -p /mnt/tmp/rhel.orig
mkdir -p /mnt/tmp/rhel.modd

cd /mnt/tmp

sudo mount -o loop /mnt/tmp/rhel-server-7.2-x86_64-dvd.iso rhel.orig


sudo cp -a rhel.orig/* rhel.modd

#cp VMwareTools
sudo mkdir -p /mnt/tmp/rhel.modd/addons/vmtools
sudo cp -a /tmp/VMwareTools-*.tar.gz  rhel.modd/addons/vmtools

sudo cp  ~/Projects/testing/kickstart/isolinux.cfg rhel.modd/isolinux/isolinux.cfg
sudo chown root.root rhel.modd/isolinux/isolinux.cfg
sudo chmod 444       rhel.modd/isolinux/isolinux.cfg

#su -c "yum -y install dvd+rw-tools genisoimage"
sudo mkisofs -R --iso-level 4 -b isolinux/isolinux.bin -c isolinux/boot.cat \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -o rhel-server-7.2-x86_64-dvd-ks.iso \
  rhel.modd

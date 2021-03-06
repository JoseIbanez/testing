#!/bin/sh
export IOU="/opt/IOU"
hostname m1
cat /etc/hosts | grep "m1$" ||  echo "127.0.0.1   m1" >> /etc/hosts

#==================================================
echo "Configure Additional Repo"
dpkg --add-architecture i386

apt-get update -y

echo "Installing deps"
apt-get install -y \
  lib32z1 lib32ncurses5 lib32bz2-1.0 \
  libssl1.0.0:i386 \
  libnet-pcap-perl libpcap0.8 \
  uml-utilities bridge-utils \
  joe python-pip expect \
  ntp

pip install awscli
pip install Jinja2

echo "Post configuration"
ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4

# Cisco %AMDP2_FE-6-EXCESSCOLL events 
sysctl -w net.unix.max_dgram_qlen=500


mkdir -p $IOU/bin
mkdir -p $IOU/scripts

if [ ! -f /home/vagrant/.aws ]; then
  cp -a /home/vagrant/.aws /root/
fi

if [ ! -f /home/ubuntu/.aws ]; then
  cp -a /home/ubuntu/.aws /root/
fi

aws --region eu-west-1 s3 sync \
    s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4/scripts \
    $IOU/scripts

echo "Generate license file"
chmod +x $IOU/scripts/*.py
chmod +x $IOU/scripts/*.bin
chmod +x $IOU/scripts/*.pl
chmod +x $IOU/bin/*

$IOU/scripts/keygen.py | grep -e 'lic' -e '=' > ~/.iourc

echo "Networking"
tunctl -t tap0
ifconfig tap0 up

brctl addbr virbr0
brctl addif virbr0 tap0

ifconfig virbr0 192.168.100.20 up
route add  -net 10.55.0.0/16 gw 192.168.100.1


echo "Syslog"
sed -i 's/^#\$UDPServerRun/\$UDPServerRun/g'  /etc/rsyslog.conf
sed -i 's/^#\$InputTCPServerRun/\$InputTCPServerRun/g'  /etc/rsyslog.conf
sed -i 's/^#\$ModLoad imudp/\$ModLoad imudp/g' /etc/rsyslog.conf
sed -i 's/^#\$ModLoad imtcp/\$ModLoad imtcp/g' /etc/rsyslog.conf
service rsyslog restart

echo "Ntp"
echo "restrict 192.168.0.0 mask 255.255.0.0 notrust" >> /etc/ntp.conf
service ntp restart

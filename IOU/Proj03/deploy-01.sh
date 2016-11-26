export IOU="/opt/IOU"

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
  joe awscli \
  ntp


echo "Post configuration"
ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4


mkdir -p $IOU
cp -a /home/vagrant/.aws /root/
aws --region eu-west-1  s3 sync s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4 $IOU

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

ifconfig virbr0 192.168.100.1 up
route add  -net 192.168.101.0/24 gw 192.168.100.1


echo "Syslog"

echo "Ntp"
echo "restrict 192.168.0.0 mask 255.255.0.0 notrust" >> /etc/ntp.conf
service ntp restart

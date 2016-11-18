export IOU="$HOME/IOU"

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
  joe awscli


echo "Post configuration"
ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4


mkdir -p $IOU
aws --region eu-west-1  s3 sync s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4 $IOU

echo "Generate license file"
chmod +x $IOU/scripts/*.py
chmod +x $IOU/scripts/*.bin
chmod +x $IOU/scripts/*.pl
chmod +x $IOU/bin/*

$IOU/scripts/keygen.py | grep -e 'lic' -e '=' > ~/.iourc

echo "Restarting"
tunctl -t tap0

brctl addbr virbr0
ifconfig virbr0 192.168.1.50 up

ifconfig tap0 up

brctl addif virbr0 tap0


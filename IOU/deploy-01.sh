export IOU="$HOME/IOU"

#==================================================
echo "Configure Additional Repo"
dpkg --add-architecture i386

apt-get update -y

echo "Installing deps"
apt-get install -y \
  lib32z1 lib32ncurses5 lib32bz2-1.0 \
  libssl1.0.0:i386 \
  joe awscli


echo "Post configuration"
ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4


aws --region eu-west-1  s3 sync s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4 $IOU

echo "Generate license file"
chmod +x $IOU/scripts/keygen.py
$IOU/scripts/keygen.py | grep -e 'lic' -e '=' > ~/.iourc





echo "Restarting"

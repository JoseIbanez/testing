apt-get install joe
IOU="~/IOU"

#==================================================
echo "Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
sudo dpkg --add-architecture i386

apt-get update -y

echo "Installing deps"
sudo apt-get install -y lib32z1 lib32ncurses5 lib32bz2-1.0
sudo apt-get install -y libssl1.0.0:i386

echo "Post configuration"
sudo ln -s /lib/i386-linux-gnu/libcrypto.so.1.0.0 /lib/libcrypto.so.4

aws s3 sync s3://fibratel.es/utils/Cisco-IOU-L2-L3-Collection-v4 $IOU/


echo "Generate license file"
$IOU/scripts/keygen.py | grep -e 'lic' -e '=' > ~/.iourc


echo "Restarting"
#sudo service mongod restart

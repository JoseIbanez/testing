#==================================================
echo "S.O. configuration ..."

cat > /etc/default/locale << EOF
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
EOF



#==================================================
echo "New repos ..."
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927

add-apt-repository -y ppa:mosquitto-dev/mosquitto-ppa

#
apt-get update -y

#==================================================
echo "Installing pakages ..."
apt-get install -y joe
apt-get install -y mosquitto-clients python-mosquitto

#sudo apt-get install -y mongodb-org

#==================================================
echo "Installing ..."
cp /vagrant/client/* ~

#==================================================
echo "Configuring app ..."
#cp /vagrant/server/prueba.conf /etc/mosquitto/conf.d/
#cp /vagrant/server/passwd /etc/mosquitto/passwd

sed -i "2i172.20.20.11  gw1.mqtt.ibanez.loc mqtt" /etc/hosts



#==================================================
echo "Restar app ..."

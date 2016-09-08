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
apt-get install -y mosquitto

#sudo apt-get install -y mongodb-org

#==================================================
echo "Installing ..."
#cp /vagrant/bin/consul /usr/local/bin/
#mkdir /etc/consul.d/
#cp /vagrant/config/demo.demo.json /etc/consul.d/demo.json
#daemon -X "consul agent -data-dir /tmp/consul -node=demo -config-dir /etc/consul.d -bind 172.20.20.15 -join 172.20.20.10"

#==================================================
echo "Configuring app ..."
#cp /vagrant/bin/demo /usr/local/bin/
#daemon -X "demo -addr=:80"
cp /vagrant/server/prueba.conf /etc/mosquitto/conf.d/
cp /vagrant/server/passwd /etc/mosquitto/passwd

mosquitto_passwd -b /etc/mosquitto/passwd thing004 1234
mosquitto_passwd -b /etc/mosquitto/passwd thing005 1234


#==================================================
echo "Restar app ..."
service mosquitto restart

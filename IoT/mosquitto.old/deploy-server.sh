#==================================================
echo "S.O. configuration ..."



#==================================================
echo "New repos ..."
add-apt-repository -y ppa:mosquitto-dev/mosquitto-ppa

#
apt-get update -y

#==================================================
echo "Installing pakages ..."
apt-get install -y mosquitto mosquitto-clients


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

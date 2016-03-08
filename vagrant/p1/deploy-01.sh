apt-get install joe

#==================================================
echo "Installing and Configuring Consul"
cp /vagrant/bin/consul /usr/local/bin/
mkdir /etc/consul.d/
cp /vagrant/config/demo.demo.json /etc/consul.d/demo.json
#daemon -X "consul agent -data-dir /tmp/consul -node=demo -config-dir /etc/consul.d -bind 172.20.20.15 -join 172.20.20.10"

#==================================================
echo "Installing and Configuring Demo App"
cp /vagrant/bin/demo /usr/local/bin/
#daemon -X "demo -addr=:80"

apt-get install joe

add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
apt-get update -y
sudo apt-get install -y mongodb-org

cat > /etc/default/locale << EOF
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
EOF


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

#!/bin/bash
#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update

#==================================================
echo "Credentials"

#BD root
cp ./my.cnf ~/.my.cnf
chmod 600 ~/.my.cnf

#1st user
source ./mysql.env

#==================================================
echo "Installing pakages"

export DEBIAN_FRONTEND="noninteractive"

debconf-set-selections <<< "mysql-server mysql-server/root_password password ${BDB_MYSQL_PASS}"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${BDB_MYSQL_PASS}"

apt-get install -y \
        mysql-server

#==================================================
echo "Post configuration"

if [ -f "/etc/mysql/my.cnf" ]; then
  sed -i 's/bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/my.cnf
fi

if [ -f "/etc/mysql/mysql.conf.d/mysqld.cnf" ]; then
  sed -i 's/bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
fi

#==================================================
echo "Restarting"
service mysql restart

#==================================================
echo "Create DB"
echo ${BDB_MYSQL_PASS}
cat ./createDB.sql | \
  sed "s/{{BDB_MYSQL_PASSWD}}/${BDB_MYSQL_PASS}/g" | \
  mysql

echo "Create table"
mysql bdb \
  -e "source createTable.sql;"

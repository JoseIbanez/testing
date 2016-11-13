#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update

export DEBIAN_FRONTEND="noninteractive"

debconf-set-selections <<< "mysql-server mysql-server/root_password password ${BDB_MYSQL_ROOT}"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${BDB_MYSQL_ROOT}"

echo "Installing deps"
apt-get install -y \
        mysql-server

echo "Post configuration"

sed -i 's/bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/my.cnf

echo "Restarting"
service mysql restart

echo "Crate DB"
cat ./createDB.sql | \
  sed "s/{{BDB_MYSQL_PASSWD}}/${BDB_MYSQL_ROOT}/g" | \
  mysql -u root -p${BDB_MYSQL_ROOT}

echo "Create table"
mysql -u root -p${BDB_MYSQL_ROOT} bdb \
  -e "source createTable.sql;"

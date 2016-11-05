#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update

debconf-set-selections <<< 'mysql-server mysql-server/root_password password passw0rd'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password passw0rd'

echo "Installing deps"
apt-get install -y \
        mysql-server

echo "Post configuration"

sed -i 's/bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/my.cnf

echo "Restarting"
service mysql restart

echo "Crate DB"

mysql -u root -ppassw0rd \
    -e "set @BDB_MYSQL_PASSWD='${BDB_MYSQL_PASS}';\
        source createDB.sql;\
        source createTable.sql;"

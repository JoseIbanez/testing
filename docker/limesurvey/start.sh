#!/bin/bash
if [ ! -f /var/www/wp-config.php ]; then
#let's create a user to ssh into
SSH_USERPASS=`pwgen -c -n -1 8`
mkdir /home/user
useradd -G sudo -d /home/user user
chown user /home/user
echo user:$SSH_USERPASS | chpasswd
echo ssh user password: $SSH_USERPASS
#mysql has to be started this way as it doesn't work to call from /etc/init.d
/usr/bin/mysqld_safe & 
sleep 10s
# Here we generate random passwords (thank you pwgen!). The first two are for mysql users, the last batch for random keys in wp-config.php
WORDPRESS_DB="wordpress"
MYSQL_PASSWORD=`pwgen -c -n -1 12`
WORDPRESS_PASSWORD=`pwgen -c -n -1 12`
#This is so the passwords show up in logs. 
echo mysql root password: $MYSQL_PASSWORD
echo wordpress password: $WORDPRESS_PASSWORD
echo $MYSQL_PASSWORD > /mysql-root-pw.txt
echo $WORDPRESS_PASSWORD > /wordpress-db-pw.txt
#there used to be a huge ugly line of sed and cat and pipe and stuff below,
#but thanks to @djfiander's thing at https://gist.github.com/djfiander/6141138
#there isn't now.


cp /var/www/ls/application/models/InstallerConfigForm.php /var/www/ls/application/models/InstallerConfigForm.php.origen

sed "/.*public \$dbpwd/s/;/ = \'$MYSQL_PASSWORD\';/
/.*public \$dbuser/s/;/ = \'root\';/" /var/www/ls/application/models/InstallerConfigForm.php.origen > /var/www/ls/application/models/InstallerConfigForm.php

mysqladmin -u root password $MYSQL_PASSWORD

killall mysqld
sleep 10s
fi
supervisord -n

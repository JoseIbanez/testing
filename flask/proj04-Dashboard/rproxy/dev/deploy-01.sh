#==================================
#Some configuration for S.O.
cp /vagrant/install/locale /etc/default/locale

#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

apt-get -y update

echo "Installing deps"
apt-get install -y \
        nginx

echo "Post configuration"
service nginx stop
sudo mv /usr/share/nginx/html /usr/share/nginx/html.orig
sudo ln -s /vagrant/rproxy/html/ /usr/share/nginx/html

rm /etc/nginx/nginx.conf
rm /etc/nginx/conf.d/default.conf

cp /vagrant/rproxy/conf/nginx.conf    /etc/nginx/nginx.conf
cp /vagrant/rproxy/conf/default.conf  /etc/nginx/conf.d/default.conf
sed -i 's/user \+nginx/user www-data/' /etc/nginx/nginx.conf


echo "127.0.0.1 kpi" >> /etc/hosts
echo "127.0.0.1 render" >> /etc/hosts


echo "Restarting"
service nginx stop
service nginx start
service nginx status

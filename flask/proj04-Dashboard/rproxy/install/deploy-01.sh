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
cp -a /vagrant/frontend/pages   /usr/share/nginx/html/
cp -a /vagrant/frontend/data    /usr/share/nginx/html/
cp -a /vagrant/frontend/js      /usr/share/nginx/html/
cp -a /vagrant/frontend/dist    /usr/share/nginx/html/
cp -a /vagrant/frontend/vendor  /usr/share/nginx/html/

cp /vagrant/rproxy/install/default    /etc/nginx/sites-available/default
cp /vagrant/rproxy/install/nginx.conf /etc/nginx/nginx.conf

echo "Restarting"
service nginx restart

# GRAFANA
#==================================
#Some configuration for S.O.
#cp /vagrant/install/locale /etc/default/locale
#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable
#sudo add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu/ saucy universe multiverse"
trusty main


sudo add-apt-repository -y "deb https://packagecloud.io/grafana/testing/debian/ jessie main"

curl https://packagecloud.io/gpg.key | sudo apt-key add -


apt-get -y update

echo "Installing deps"
apt-get install -y \
        git nano curl\
        grafana

echo "Post configuration"

sudo update-rc.d grafana-server defaults 95 10


echo "Restarting"
sudo service grafana-server start


#==================================================
echo "Configure Additional Repo"
#sudo add-apt-repository -y ppa:ubuntu-lxc/lxd-stable

sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

#echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list




apt-get -y update


echo "Installing packages"
apt-get install -y \
        docker-engine \
        jq


echo "Post configuration"

curl -L https://github.com/docker/machine/releases/download/v0.8.2/docker-machine-`uname -s`-`uname -m` >/usr/local/bin/docker-machine && \
chmod +x /usr/local/bin/docker-machine

sudo groupadd docker
usermod -aG docker $USER


echo "Restarting"

apt-get install joe

cp /vagrant/config/locale /etc/default/locale

#==================================================
echo "##Configure Additional Repo"
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
#add-apt-repository "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"

wget -q -O - http://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -

add-apt-repository "deb http://pkg.jenkins.io/debian binary/"


apt-get update -y
echo "##Installing pkg"

sudo apt-get install -y jenkins

echo "##Post configuration"



cp -a /vagrant/scripts ./

echo "##Generate license file"

echo "##Restarting"
#sudo service mongod restart

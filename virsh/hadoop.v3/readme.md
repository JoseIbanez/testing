
https://utho.com/docs/database/hadoop/setting-up-a-hadoop-cluster/
https://medium.com/@abhikdey06/apache-hadoop-3-3-6-installation-on-ubuntu-22-04-14516bceec85


cat hosts | sudo tee -a /etc/hosts

# Create hadoop user
sudo adduser --disabled-password --gecos "" hdoop
echo 'hdoop:hdoop' | sudo chpasswd
sudo adduser hdoop sudo

sudo su hdoop
cd
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

cp ~/.ssh/id_rsa.pub ~/.ssh/master.pub
cat ~/.ssh/master.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh localhost

# Install java
sudo apt update -y
sudo apt upgrade -y
sudo apt install openjdk-11-jdk -y


# Install
mkdir downloads
cd downloads
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.4/hadoop-3.2.4.tar.gz
tar xzf hadoop-3.2.4.tar.gz

sudo mkdir /usr/local/hadoop
sudo chown hdoop:hdoop /usr/local/hadoop/
mv hadoop-3.2.4/* /usr/local/hadoop/


# copy config
cd
cat ./config/bashrc.sh >> .bashrc 
source .bashrc 
cp ./config/core-site.xml /usr/local/hadoop/etc/hadoop/core-site.xml 
cp ./config/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh 
cp ./config/hdfs-site.xml /usr/local/hadoop/etc/hadoop/hdfs-site.xml 
cp ./config/mapred-site.xml /usr/local/hadoop/etc/hadoop/mapred-site.xml 
cp ./config/yarn-site.xml /usr/local/hadoop/etc/hadoop/yarn-site.xml 
cp ./config/workers /usr/local/hadoop/etc/hadoop/workers 
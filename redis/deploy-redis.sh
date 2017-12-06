apt-get -y update
apt-get install -y build-essential tcl

apt install -y ruby
gem install redis


cd /tmp
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable

make
make test
sudo make install

cd 7000
screen -dmS redis7000 /tmp/redis-server redis.conf
cd ../7001
screen -dmS redis7001 /tmp/redis-server redis.conf
cd ../7002
screen -dmS redis7002 /tmp/redis-server redis.conf
cd ../7003
screen -dmS redis7003 /tmp/redis-server redis.conf
cd ../7004
screen -dmS redis7004 /tmp/redis-server redis.conf
cd ../7005
screen -dmS redis7005 /tmp/redis-server redis.conf


./redis-trib.rb create --replicas 1 \
         10.28.1.102:7000 \
         10.28.1.102:7001 \
         10.28.1.102:7002 \
         10.28.1.102:7003 \
         10.28.1.102:7004 \
         10.28.1.102:7005 \
         10.28.1.103:7000 \
         10.28.1.103:7001 \
         10.28.1.103:7002 \
         10.28.1.103:7003 \
         10.28.1.103:7004 \
         10.28.1.103:7005



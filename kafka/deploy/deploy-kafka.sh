#!/bin/bash

cd downloads

wget "https://ftp.cixug.es/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz"

tar -xzf kafka_2.13-2.6.0.tgz
cd kafka_2.13-2.6.0


screen -d -m -S zoo \
./bin/zookeeper-server-start.sh config/zookeeper.properties

screen -d -m -S kafka \
./bin/kafka-server-start.sh config/server.properties


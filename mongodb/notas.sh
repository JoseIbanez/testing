#!/bin/bash

#common
apt-get update -y
apt-get install -y mongodb
mkdir -p /mnt/mongo/db1
mkdir -p /mnt/mongo/db2
mkdir -p /mnt/mongo/db3

#Replica set rs0

mongod --bind_ip 0.0.0.0 --port 30001 --replSet rs0 --dbpath /mnt/mongo/db1 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db1/mongo.log --shardsvr --fork
mongod --bind_ip 0.0.0.0 --port 30002 --replSet rs0 --dbpath /mnt/mongo/db2 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db2/mongo.log --shardsvr --fork
mongod --bind_ip 0.0.0.0 --port 30003 --replSet rs0 --dbpath /mnt/mongo/db3 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db3/mongo.log --shardsvr --fork


myIP="10.24.13.208"
rs.initiate( {
   _id: "rs0",
   members: [
      { _id: 0, host: myIP+":30001" },
      { _id: 1, host: myIP+":30002" },
      { _id: 2, host: myIP+":30003" }
   ]
} )

#Replica set rs1

mongod --bind_ip 0.0.0.0 --port 30001 --replSet rs1 --dbpath /mnt/mongo/db1 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db1/mongo.log --shardsvr --fork
mongod --bind_ip 0.0.0.0 --port 30002 --replSet rs1 --dbpath /mnt/mongo/db2 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db2/mongo.log --shardsvr --fork
mongod --bind_ip 0.0.0.0 --port 30003 --replSet rs1 --dbpath /mnt/mongo/db3 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db3/mongo.log --shardsvr --fork


myIP="10.24.13.203"
rs.initiate( {
   _id: "rs1",
   members: [
      { _id: 0, host: myIP+":30001" },
      { _id: 1, host: myIP+":30002" },
      { _id: 2, host: myIP+":30003" }
   ]
} )




#config server 

mongod --bind_ip 0.0.0.0 --port 30001 --replSet rsC --dbpath /mnt/mongo/db1 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db1/mongo.log --configsvr --fork
mongod --bind_ip 0.0.0.0 --port 30002 --replSet rsC --dbpath /mnt/mongo/db2 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db2/mongo.log --configsvr --fork
mongod --bind_ip 0.0.0.0 --port 30003 --replSet rsC --dbpath /mnt/mongo/db3 --smallfiles --oplogSize 50 --logpath /mnt/mongo/db3/mongo.log --configsvr --fork

myIP="10.24.13.128"
rs.initiate( {
   _id: "rsC",
   configsvr: true,
   members: [
      { _id: 0, host: myIP+":30001" },
      { _id: 1, host: myIP+":30002" },
      { _id: 2, host: myIP+":30003" }
   ]
} )


#mongos 
mkdir -p /mnt/mongo/s1
mongos --port 30000 --configdb rsC/10.24.13.128:30001 --logpath /mnt/mongo/s1/mongo.log --fork




sh.addShard( "rs0/10.24.13.208:30001" )
sh.addShard( "rs1/10.24.13.203:30001" )



for (var i = 0; i<2000 ; i++) {
    db.tester.insert({"foo":"bar","baz":i, "z":10-i})
}


db.adminCommand( { shardCollection: "records.people", key: { "zipcode": 1 } } )

db.people.insert({"name":"paco","baz":1, "zipcode":1})


sh.enableSharding("records")
db.people.ensureIndex(zipcode)
sh.shardCollection( "records.people", { "zipcode" : "hashed" } )

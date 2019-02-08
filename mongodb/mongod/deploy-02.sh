#
# http://www.mongodbspain.com/es/2015/01/26/how-to-set-up-a-mongodb-sharded-cluster/
#


#Create dirs
sudo mkdir -p /var/lib/mongodb/shardedcluster
sudo chown ubuntu.ubuntu /var/lib/mongodb/shardedcluster

mkdir /var/lib/mongodb/shardedcluster/cfg0
mkdir /var/lib/mongodb/shardedcluster/cfg1
mkdir /var/lib/mongodb/shardedcluster/cfg2
mkdir /var/lib/mongodb/shardedcluster/a0
mkdir /var/lib/mongodb/shardedcluster/a1
mkdir /var/lib/mongodb/shardedcluster/a2
mkdir /var/lib/mongodb/shardedcluster/b0
mkdir /var/lib/mongodb/shardedcluster/b1
mkdir /var/lib/mongodb/shardedcluster/b2

mkdir /var/lib/mongodb/shardedcluster/c0
mkdir /var/lib/mongodb/shardedcluster/c1
mkdir /var/lib/mongodb/shardedcluster/c2
mkdir /var/lib/mongodb/shardedcluster/c3
mkdir /var/lib/mongodb/shardedcluster/c4
mkdir /var/lib/mongodb/shardedcluster/c5
mkdir /var/lib/mongodb/shardedcluster/c6
mkdir /var/lib/mongodb/shardedcluster/c7
mkdir /var/lib/mongodb/shardedcluster/c8
mkdir /var/lib/mongodb/shardedcluster/c9



#Config servers
mongod --configsvr --port 26050 --logpath /var/lib/mongodb/shardedcluster/log.cfg0 --logappend --dbpath /var/lib/mongodb/shardedcluster/cfg0 --fork
mongod --configsvr --port 26051 --logpath /var/lib/mongodb/shardedcluster/log.cfg1 --logappend --dbpath /var/lib/mongodb/shardedcluster/cfg1 --fork
mongod --configsvr --port 26052 --logpath /var/lib/mongodb/shardedcluster/log.cfg2 --logappend --dbpath /var/lib/mongodb/shardedcluster/cfg2 --fork

#Replica Server: a
mongod --shardsvr --replSet a --dbpath /var/lib/mongodb/shardedcluster/a0 --logpath /var/lib/mongodb/shardedcluster/log.a0 --port 27010 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --replSet a --dbpath /var/lib/mongodb/shardedcluster/a1 --logpath /var/lib/mongodb/shardedcluster/log.a1 --port 27011 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --replSet a --dbpath /var/lib/mongodb/shardedcluster/a2 --logpath /var/lib/mongodb/shardedcluster/log.a2 --port 27012 --fork --logappend --smallfiles --oplogSize 50

#Replica Server: b
mongod --shardsvr --replSet b --dbpath /var/lib/mongodb/shardedcluster/b0 --logpath /var/lib/mongodb/shardedcluster/log.b0 --port 27020 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --replSet b --dbpath /var/lib/mongodb/shardedcluster/b1 --logpath /var/lib/mongodb/shardedcluster/log.b1 --port 27021 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --replSet b --dbpath /var/lib/mongodb/shardedcluster/b2 --logpath /var/lib/mongodb/shardedcluster/log.b2 --port 27022 --fork --logappend --smallfiles --oplogSize 50

#Without Replica
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c0 --logpath /var/lib/mongodb/shardedcluster/log.c0 --port 27030 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c1 --logpath /var/lib/mongodb/shardedcluster/log.c1 --port 27031 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c2 --logpath /var/lib/mongodb/shardedcluster/log.c2 --port 27032 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c3 --logpath /var/lib/mongodb/shardedcluster/log.c3 --port 27033 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c4 --logpath /var/lib/mongodb/shardedcluster/log.c4 --port 27034 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c5 --logpath /var/lib/mongodb/shardedcluster/log.c5 --port 27035 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c6 --logpath /var/lib/mongodb/shardedcluster/log.c6 --port 27036 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c7 --logpath /var/lib/mongodb/shardedcluster/log.c7 --port 27037 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c8 --logpath /var/lib/mongodb/shardedcluster/log.c8 --port 27038 --fork --logappend --smallfiles --oplogSize 50
mongod --shardsvr --dbpath /var/lib/mongodb/shardedcluster/c9 --logpath /var/lib/mongodb/shardedcluster/log.c9 --port 27039 --fork --logappend --smallfiles --oplogSize 50


#Route Servers
mongos --configdb localhost:26050,localhost:26051,localhost:26052 --fork --logappend --logpath /var/lib/mongodb/shardedcluster/log.mongos0
mongos --configdb localhost:26050,localhost:26051,localhost:26052 --fork --logappend --logpath /var/lib/mongodb/shardedcluster/log.mongos1 --port 26061




ps -ef | grep mongo



#initiate replica a
mongo --port 27010

rs.initiate(
   {
      _id: "a",
      version: 1,
      members: [
         { _id: 0, host : "localhost:27010" },
         { _id: 1, host : "localhost:27011" },
         { _id: 2, host : "localhost:27012" }
      ]
   }
)


#initiate replica b
mongo --port 27020

rs.initiate(
   {
      _id: "b",
      version: 1,
      members: [
         { _id: 0, host : "localhost:27020" },
         { _id: 1, host : "localhost:27021" },
         { _id: 2, host : "localhost:27022" }
      ]
   }
)


############################################

#shardering

sh.status()
sh.addShard("a/localhost:27010")
sh.addShard("b/localhost:27020")

sh.addShard("localhost:27030")
sh.addShard("localhost:27031")
sh.addShard("localhost:27032")
sh.addShard("localhost:27033")
sh.addShard("localhost:27034")
sh.addShard("localhost:27035")
sh.addShard("localhost:27036")
sh.addShard("localhost:27037")
sh.addShard("localhost:27038")
sh.addShard("localhost:27039")

sh.status()

sh.getBalancerState()



use test
sh.enableSharding("test")

db.harry.ensureIndex( { _id : "hashed" } )

sh.shardCollection("test.harry", { "_id": "hashed" } )

for (var i = 0; i<100000 ; i++) {
db.harry.insert({"foo":"bar","baz":i, "z":10-i})
}

sh.status({"verbose":true})
sh.status()

use admin
db.runCommand( { removeShard: "localhost27033" } )

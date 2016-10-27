#!/bin/sh
docker network create -d overlay bdbnet

docker service create \
  --replicas 1 \
  --name kpi \
  --network bdbnet \
  --publish 8010:8010 \
  --env BDB_MYSQL_DB=$BDB_MYSQL_DB \
  --env BDB_MYSQL_HOST=$BDB_MYSQL_HOST \
  --env BDB_MYSQL_PASS=$BDB_MYSQL_PASS \
  --env BDB_MYSQL_USER=$BDB_MYSQL_USER \
  ibanez/bdb_kpi:1.1

curl http://localhost:8010
docker ps | grep bdb_kpi | cut -d ' ' -f 1 | xargs docker logs

####

docker service create \
    --replicas 1 \
    --name render \
    --network bdbnet \
    --env BDB_MYSQL_DB=$BDB_MYSQL_DB \
    --env BDB_MYSQL_HOST=$BDB_MYSQL_HOST \
    --env BDB_MYSQL_PASS=$BDB_MYSQL_PASS \
    --env BDB_MYSQL_USER=$BDB_MYSQL_USER \
    ibanez/bdb_render:1.0

curl http://localhost:8000
docker ps | grep bdb_render | cut -d ' ' -f 1 | xargs docker logs

####

docker service create \
    --replicas 1 \
    --name rproxy \
    --network bdbnet \
    --publish 80:80 \
    --network bdbnet \
    ibanez/bdb_rproxy:1.3

docker service update --image ibanez/bdb_rproxy:1.2 bdb_rproxy

curl http://localhost
docker ps | grep bdb_rproxy | cut -d ' ' -f 1 | xargs docker logs

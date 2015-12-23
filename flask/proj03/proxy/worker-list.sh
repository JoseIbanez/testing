#!/bin/sh

echo "upstream app_servers {" > ./servers.lst
docker inspect --format='   server {{.NetworkSettings.Networks.bridge.IPAddress}}:8000;' $(docker ps -q --filter name=worker) >> ./servers.lst
echo "}" >> ./servers.lst

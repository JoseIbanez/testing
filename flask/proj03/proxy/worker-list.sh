#!/bin/sh
docker inspect --format=' server {{.NetworkSettings.Networks.bridge.IPAddress}}:8000' $(docker ps -q --filter name=worker)

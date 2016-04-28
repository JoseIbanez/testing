#!/bin/sh

consulSrv=$1

apt-get install -y daemon curl dnsutils daemon



daemon -O local0.info -- consul agent -server -data-dir="/tmp/consul" -bootstrap-expect 3

echo "Joining to $consulSrv"
consul join $consulSrv

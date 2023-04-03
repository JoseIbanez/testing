#!/bin/bash

set -e

LIST="/home/ibanez/Projects/testing/zeronet/listas/ramses.m3u8"

# Acelink ID
ID=`echo ${1} | sed 's@.*//@@'`
if [ "${#ID}" -lt "40" ]; then
  grep -A1 "Lucas.*${1}" ${LIST} | head -n2

  FULLID=`grep -A1 "Lucas.*${1}" ${LIST} | grep -v EXTINF | head -n1 | tr -d '\r'`
  ID=`echo $FULLID | sed 's@.*//@@'`
fi
echo "$1:$ID:"


# Client port
if [ -n "$2" ]; then
  PORT=$2
else
  PORT="3200"
fi
echo "Client Port: $PORT"


# Peer port
if [ -n "$3" ]; then
  PEERPORT="-p 8621:8621"
else
  PEERPORT=""
fi


#######
mkdir -p /mnt/d1/hls/$PORT
mkdir -p /mnt/d1/hls-log/$PORT

docker ps -q -f name="acelink.$PORT" | grep . && docker kill "acelink.$PORT" 
sleep 3

docker run -d --rm  \
    -v /mnt/d1/hls/$PORT:/mnt/hls \
    -e "ID=$ID"  \
    --name "acelink.$PORT" \
    -p $PORT:6878 $PEERPORT \
    --cap-add=NET_ADMIN \
    acelink-ffmpeg

#./test-acestream.py --duration 5 -p $PORT

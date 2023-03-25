#!/bin/bash

# Acelink ID
ID=`echo $1 | sed 's@.*//@@'`


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

docker kill "acelink.$PORT" | echo ""
sleep 3

docker run -d --rm  \
    -v /mnt/d1/hls/$PORT:/mnt/hls \
    -e "ID=$ID"  \
    --name "acelink.$PORT" \
    -p $PORT:6878 $PEERPORT \
    --cap-add=NET_ADMIN \
    acelink-ffmpeg

./test-acestream.py --duration 5 -p $PORT

#!/bin/bash

# Client port
if [ -n "$2" ]; then
  PORT=$2
  FOLDER=$2
else
  PORT=6878
  FOLDER=3231
fi
echo "Client Port: $PORT"

# Peer port
if [ -n "$3" ]; then
  PEERPORT=8621
else
  PEERPORT=
fi


# Check screen


# Check docker image
DCKID=`docker ps | grep "acelink.$PORT"`
echo "Docker $DCKID"
if [ -z "$DCKID" ]&&[ -n "$PEERPORT" ]; then
  docker run -d --rm --name "acelink.$PORT" -p $PORT:6878 -p $PEERPORT:8621 --cap-add=NET_ADMIN blaiseio/acelink
  docker exec -t acelink.$PORT sh -c "apt-get update; apt-get install -y iproute2" 
  docker exec -t acelink.$PORT sh -c "tc qdisc add dev eth0 root tbf rate 100mbit burst 40mbit latency 400ms"
  docker exec -t acelink.$PORT sh -c "tc qdisc show dev eth0"
  sleep 5

elif [ -z "$DCKID" ]; then
  docker run -d --rm --name "acelink.$PORT" -p $PORT:6878 blaiseio/acelink
  sleep 5
fi


if [ -n "$1" ]; then
  ID=`echo $1 | sed 's@.*//@@'`
fi

mkdir -p /mnt/d1/hls/$FOLDER/
cd /mnt/d1/hls/$FOLDER/
rm -f *.ts
rm -f *.m3u8

echo $ID  > id

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:$PORT/ace/getstream?id=$ID"


screen -ls | grep "acelink.$PORT" | cut -d. -f1 | xargs -n 1 -r kill
screen -dm -S "acelink.$PORT" \
ffmpeg \
 -i $ACE_URL \
 -map 0 -c copy \
 -c:a ac3 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8

screen -ls
sleep 1
ls -l *

test-acestream --port $PORT --duration 5

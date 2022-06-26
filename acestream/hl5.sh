#!/bin/bash

if [ -n "$2" ]; then
  PORT=$2
  FOLDER=$2
else
  PORT=6878
  FOLDER=3231
fi

echo "Port: $PORT"

# Check screen


# Check docker image
DCKID=`docker ps | grep "acelink.$PORT"`
echo "Docker $DCKID"
if [ -z "$DCKID" ]; then
  docker run -d --name "acelink.$PORT" -p $PORT:6878 blaiseio/acelink
  sleep 5
fi


if [ -n "$1" ]; then
  ID=`echo $1 | sed 's@.*//@@'`
fi

mkdir -p /tmp/d1/hls/$FOLDER/
cd /tmp/d1/hls/$FOLDER/
rm -f *.ts
rm -f *.m3u8

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:$PORT/ace/getstream?id=$ID"


screen -ls | grep "acelink.$PORT" | cut -d. -f1 | xargs kill
screen -dm -S "acelink.$PORT" \
ffmpeg \
 -i $ACE_URL \
 -c copy -map 0 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8

screen -ls

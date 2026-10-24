#!/bin/bash

set -e


export ID=d65257bb934b73647374224fd62d836815804be2
#export ID=14407b00d454cb7dc0d70aa26e8bbc554f457f00
export PORT=3350


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
    acelink-ffmpeg-2


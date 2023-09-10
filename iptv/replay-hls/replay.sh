#!/bin/bash

CHANNEL_ID=$1
MEDIA_URL=$2

mkdir -p "/opt/hls/$CHANNEL_ID"
cd "/opt/hls/$CHANNEL_ID"

while true; do

   rm *.ts *.m3u8
   tsprefix=`date +%d%H%M`


   ffmpeg \
     -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -re  \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a ac3 \
     -f hls \
     -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
     -hls_segment_filename "d${tsprefix}stream%d.ts" \
     -hls_init_time 4 -hls_time 4 \
     stream.m3u8

   sleep 30

done



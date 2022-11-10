#!/bin/bash

cd /mnt/hls/
rm -f *.ts
rm -f *.m3u8
rm -f *.vtt

echo $ID  > id

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:6878/ace/getstream?id=$ID"

#    -map 0:v:0 -map 0:a:1 \
#        -c:a ac3 \

while true; do

    ffmpeg \
    -i $ACE_URL \
    -map 0:v:0 -map 0:a:0 \
    -c:v copy \
    -c:a ac3 \
    -f hls \
    -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
    -hls_init_time 4 -hls_time 4 \
    stream.m3u8

    sleep 5

done
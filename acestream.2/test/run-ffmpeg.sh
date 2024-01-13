#!/bin/bash

set -e

cd /mnt/d1/hls/

mkdir -p 3288
cd ./3288

rm -f *.ts
rm -f *.m3u8
rm -f *.vtt

export ID=5e4cd48c79f991fcbee2de8b9d30c4b16de3b952
echo $ID  > id

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:6878/ace/getstream?id=$ID"



tsprefix=`date +%d%H%M`

ffmpeg \
-i $ACE_URL \
-map 0:v:0 -map 0:a:0 \
-c:v copy \
-c:a ac3 \
-f hls \
-hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
-hls_segment_filename "d${tsprefix}stream%d.ts" \
-hls_init_time 4 -hls_time 4 \
stream.m3u8

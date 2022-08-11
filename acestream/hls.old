#!/bin/bash



# Check docker image
DCKID=`docker ps | grep acelink`
echo "Docker $DCKID"
if [ -z "$DCKID" ]; then
  docker run -d --name acelink -p 6878:6878 blaiseio/acelink
  sleep 5
fi


if [ -n "$1" ]; then
  ID=`echo $1 | sed 's@.*//@@'`
fi

cd /mnt/d1/hls/3231/
rm -f *.ts
rm -f *.m3u8

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:6878/ace/getstream?id=$ID"

ffmpeg \
 -i $ACE_URL \
 -c copy -map 0 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8


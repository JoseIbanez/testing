#!/bin/bash


export MEDIA_URL="http://127.0.0.1:8800/3231/stream.m3u8"
export STREAM_URL=$(pass telegram/STREAM_URL)
export STREAM_KEY=$(pass telegram/STREAM_KEY)

# Kick
ffmpeg \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
     -f flv $STREAM_URL$STREAM_KEY








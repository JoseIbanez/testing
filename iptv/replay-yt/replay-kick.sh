#!/bin/bash


export MEDIA_URL="http://127.0.0.1:8800/3232/stream.m3u8"
export KICK_URL=$(pass kick/vlan200/KICK_URL)
export KICK_KEY=$(pass kick/vlan200/KICK_KEY)

# Kick
ffmpeg \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
     -f flv $KICK_URL/app/$KICK_KEY








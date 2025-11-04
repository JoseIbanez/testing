#!/bin/bash


export MEDIA_URL="http://192.168.1.20:8800/3231/stream.m3u8"

export MEDIA_URL="http://127.0.0.1:8800/3231/stream.m3u8"

# YouTube
ffmpeg \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
     -f flv rtmp://a.rtmp.youtube.com/live2/$CHANNELID

# Kick
ffmpeg \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
     -f flv $KICK_URL/app/$KICK_KEY



# Telegram
ffmpeg -stream_loop -1 -re \
     -i $MEDIA_URL \
     -c:v libx264 -preset veryfast -b:v 3500k \
     -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -g 50 \
     -c:a aac -b:a 160k -ac 2 -ar 44100 \
     -f flv $TELEGRAM_URL/s/$TELEGRAM_KEY



# VK
ffmpeg \
     -i $MEDIA_URL \
     -map 0:v:0 -map 0:a:0 \
     -c:v copy \
     -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
     -f flv $VK_URL/$VK_KEY




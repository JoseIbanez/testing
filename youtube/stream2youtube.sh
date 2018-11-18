#!/bin/bash

#https://www.youtube.com/watch?v=BWjPSRFYXV0

source ~/.secrets/youtube/channelId.sh

#v4l2-ctl --set-fmt-video=width=1920,height=1080,pixelformat=YUYV -d /dev/video1
v4l2-ctl --set-fmt-video=width=1280,height=720,pixelformat=YUYV -d /dev/video1

ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono \
       -f v4l2 -r 10 -i /dev/video1 -c:v libx264 -pix_fmt yuv420p \
       -preset ultrafast -g 20 -b:v 2500k \
       -c:a aac -ar 44100 -threads 0 -bufsize 512k -strict experimental \
       -f flv rtmp://a.rtmp.youtube.com/live2/$CHANNELID

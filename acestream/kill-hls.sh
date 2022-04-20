#!/bin/bash

# Check ffmpeg process get PID
ps -ef | grep ffmpeg.*hls | grep -v grep
HLSPID=`ps -ef | grep ffmpeg.*hls | grep -v grep | awk '{print $2}'`

# Kill ffmpeg
echo "kill -9 $HLSPID"
kill -9 $HLSPID

# Kill and rm acelink
docker ps
docker kill acelink
docker rm   acelink

docker ps




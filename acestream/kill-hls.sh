#!/bin/bash

# Check ffmpeg process get PID
screen -ls | grep acelink | cut -d. -f1 | xargs kill

# Kill and rm acelink
docker ps -aq -f "name=acelink" | xargs -n 1 docker kill
docker ps -aq -f "name=acelink" | xargs -n 1 docker rm

#Docker
docker ps

#Screen
screen -ls


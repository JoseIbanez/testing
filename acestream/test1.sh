#!/bin/bash

https://hub.docker.com/r/bfayers/docker-acestream-proxy

docker run -d -p 8000:8000 -e "UPLOAD_LIMIT=2000" -e "DOWNLOAD_LIMIT=8000" --name aceproxy bfayers/docker-acestream-proxy

vlc http://127.0.0.1:8000/pid/STREAMID/stream.mp4
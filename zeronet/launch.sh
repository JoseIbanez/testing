#!/bin/sh
docker run -d \
  -e "ENABLE_TOR=true" \
  -v ~/Downloads/zeronet:/root/data \
  -p 15441:15441 \
  -p 127.0.0.1:43110:43110 \
  nofish/zeronet


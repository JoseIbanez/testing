#!/bin/sh
docker run -d --rm \
  --name zeronet \
  -e "ENABLE_TOR=true" \
  -v ~/Downloads/zeronet:/root/data \
  -p 15441:15441 \
  -p 43110:43110 \
  nofish/zeronet


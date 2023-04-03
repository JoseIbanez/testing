#!/bin/bash

export TOKEN="MAGIC"

curl localhost:5000/hls/2333/ \
    -H "Authorization: Bearer $TOKEN"

curl -X PUT  http://localhost:5000/hls/3333/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $TOKEN" \
    -d'{"ace_id":"AAAA", "description": "La 2" }'


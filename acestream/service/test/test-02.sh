#!/bin/bash

export TOKEN="MAGIC"

curl -X PUT  http://localhost:5000/hls/3251/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $TOKEN" \
    -d'{"ace_id":"c9ee7c95e7a2e9cd0e848b1f70848453652bebc2", "description": "La 2" }'

sleep 20

curl -X DELETE  http://localhost:5000/hls/3251/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $TOKEN" 

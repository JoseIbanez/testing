#!/bin/bash

export TOKEN="MAGIC"

curl -X GET http://localhost:5000/hls/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -H "Authorization: Bearer $TOKEN" 

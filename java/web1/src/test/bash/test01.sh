#!/bin/bash

echo "---- Test 1 ----"

curl -X POST \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car \
     -d '{ "maker": "Seat" }'
echo ""

echo "---- Test 2 ----"
curl -X POST \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car \
     -d '{ "maker": "Seat", "plate":"M8033XY", "serialNumber": "96202704-53d5-48f8-a064-29e73067b8e0" }'
echo ""

echo "---- Test 3 ----"
curl \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car \
    | jq .

echo "---- Test 4 ----"
curl \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car/M8033XY \
    | jq .



echo "---- Test 5 ----"
curl \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car/96202704-53d5-48f8-a064-29e73067b8e0 \
    | jq .


echo "---- Test 6 ----"
curl \
    -H "Content-Type: application/json" \
     http://localhost:8080/api/v1/car/FAKE \
    | jq .

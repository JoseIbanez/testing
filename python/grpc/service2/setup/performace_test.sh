#!/bin/bash

brew install ghz

ghz --insecure --async \
  --proto ./protos/service.proto \
  --call Collector/SendEvent \
  -c 10 -n 10000 --rps 200 \
  -d '{"opco":"{{.WorkerID}}"}' 0.0.0.0:50051
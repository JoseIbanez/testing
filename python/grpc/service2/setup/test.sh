#!/bin/bash

# DNS takes long time
export GRPC_DNS_RESOLVER=native


grpcurl -import-path ../protos -proto service.proto list
grpcurl -import-path ../protos -proto service.proto list collector.Collector

grpcurl \
  -import-path ../protos -proto service.proto \
  -d '{"opco": "vf-es"}' \
  -plaintext h3.local:50051 collector.Collector/SendEvent


grpcurl \
  -insecure \
  -import-path ../protos -proto service.proto \
  -d '{"opco": "vf-es"}' \
  h3.loc:443 collector.Collector/SendEvent

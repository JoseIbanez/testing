#!/bin/bash

curl http://localhost:8500/v1/health/state/critical | python -m json.tool
curl -v http://localhost:8500/v1/kv/?recurse | python -m json.tool
curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key1
curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key2?flags=42
curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/sub/key3
curl http://localhost:8500/v1/kv/?recurse | python -m json.tool

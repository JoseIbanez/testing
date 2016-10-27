#!/bin/sh

docker build -t ibanez/bdb_kpi:1.0    -t ibanez/bdb_kpi    ../../kpi/
docker push ibanez/bdb_kpi:1.1

docker build -t ibanez/bdb_render:1.0 -t ibanez/bdb_render ../../render/
docker push ibanez/bdb_render:1.0

docker build -t ibanez/bdb_rproxy:1.3 -t ibanez/bdb_rproxy ../../rproxy/
docker push ibanez/bdb_rproxy:1.3

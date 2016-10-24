#!/bin/sh

docker build -t ibanez/bdb_kpi:1.0    -t ibanez/bdb_kpi    ../../kpi/
docker build -t ibanez/bdb_render:1.0 -t ibanez/bdb_render ../../render/

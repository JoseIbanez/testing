#!/bin/bash
. ./scripts/.env
./scripts/elastic-dump -d $1 -s 24 -i "cisco-meraki-tmf688-metric-*" -o /mnt/d2/esdumps/meraki-

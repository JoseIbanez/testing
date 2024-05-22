#!/bin/bash

mkdir -p /dev/disk/by-id
/opt/acestream/start-engine --client-console --bind-all --live-cache-type memory

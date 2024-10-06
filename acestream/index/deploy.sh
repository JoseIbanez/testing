#!/bin/bash

set -e
source ~/py/v311/bin/activate

grip index.md  --export index.html
cp index.html /mnt/d1/hls/streams/


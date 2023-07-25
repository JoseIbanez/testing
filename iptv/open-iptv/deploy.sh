#!/bin/bash

set -e
source ~/py-venv/bin/activate

grip index.md  --export index.html
cp index.html /mnt/d1/hls/open/



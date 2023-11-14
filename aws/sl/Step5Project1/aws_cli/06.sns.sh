#!/bin/bash
set -e

# Create SNS (queue() to delete files
aws sns create-topic \
    --name $SNS_DEL \
    > out/sns_del.json
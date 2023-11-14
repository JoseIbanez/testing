#!/bin/bash
set -e

# Create queue
aws sqs create-queue --queue-name  $SQS_INC > out/sqs_inc.json

export SQS_URL_INC=`cat out/sqs_inc.json | jq -r .QueueUrl`

# Set policy for Incoming Queue
envsubst < sqs_policy_inc.json > out/sqs_policy_inc.json
export SQS_POLICY=`cat out/sqs_policy_inc.json | jq -c .| jq -Rsa .`

envsubst < sqs_attr_inc.json > out/sqs_attr_inc.json
aws sqs set-queue-attributes --queue-url $SQS_URL_INC --attributes file://out/sqs_attr_inc.json


# Export SQS ARNs and others params
aws sqs get-queue-attributes --queue-url $SQS_URL_INC --attribute-names All > out/sqs_attr_inc.json


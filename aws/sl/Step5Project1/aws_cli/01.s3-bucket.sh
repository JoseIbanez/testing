#!/bin/bash
set -e

# Incoming Bucket
aws s3api create-bucket \
    --bucket $BUCKET_INC \
    > out/s3_inc.json

envsubst < bucket_policy_inc.json > out/bucket_policy_inc.json
envsubst < bucket_cors.json   > out/bucket_cors.json

aws s3api put-bucket-policy --bucket $BUCKET_INC --policy file://out/bucket_policy_inc.json
aws s3api put-bucket-cors   --bucket $BUCKET_INC --cors-configuration file://out/bucket_cors.json


# Deleted Bucket
aws s3api create-bucket \
    --bucket $BUCKET_DEL \
    > out/s3_del.json


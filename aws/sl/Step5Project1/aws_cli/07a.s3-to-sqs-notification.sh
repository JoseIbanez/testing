#!/bin/bash
set -e

# GET AWS_ACCOUNT
aws sts get-caller-identity --query "Account" --output text > out/aws_account.txt
export AWS_ACCOUNT=`cat out/aws_account.txt`

# Attach an Inline Policy 
envsubst < bucket_notification_inc.json > out/bucket_notification_inc.json


# S3 notification
aws s3api put-bucket-notification-configuration \
    --bucket $BUCKET_INC \
    --notification-configuration file://out/bucket_notification_inc.json


#!/bin/bash
set -e

#GET AWS ACCOUNT
export AWS_ACCOUNT=`cat out/aws_account.txt`

# SNS ARN
export SNS_DEL_ARN=`cat out/sns_del.json | jq -r .TopicArn`

# Create SES RULE SET
aws ses create-receipt-rule-set \
    --rule-set-name "delete_file"

# Create SES RULE
envsubst < ses_rule.json > out/ses_rule.json
aws ses create-receipt-rule \
    --cli-input-json file://out/ses_rule.json

# Activate SES RULE SET
aws ses set-active-receipt-rule-set \
    --rule-set-name "delete_file"

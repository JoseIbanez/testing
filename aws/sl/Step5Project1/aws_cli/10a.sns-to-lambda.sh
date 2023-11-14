#!/bin/bash
set -e

#GET AWS ACCOUNT
export AWS_ACCOUNT=`cat out/aws_account.txt`

# SNS & LAMDA ARN
export SNS_DEL_ARN=`cat out/sns_del.json | jq -r .TopicArn`
export LAMBDA_DEL_ARN=`cat out/lambda_function_del.json | jq -r .FunctionArn`

aws lambda add-permission \
    --function-name $LAMBDA_DEL \
    --source-arn $SNS_DEL_ARN \
    --statement-id function-with-sns \
    --action "lambda:InvokeFunction" \
    --principal sns.amazonaws.com 

aws sns subscribe --protocol lambda \
    --topic-arn $SNS_DEL_ARN \
    --notification-endpoint $LAMBDA_DEL_ARN 



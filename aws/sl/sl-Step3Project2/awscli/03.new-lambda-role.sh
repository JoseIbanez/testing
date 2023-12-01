#!/bin/bash
set -e

export DYNAMODBWRITE_POLICY="DynamoDBWriteAccess"


# GET AWS_ACCOUNT
aws sts get-caller-identity --query "Account" --output text > out/aws_account.txt
export AWS_ACCOUNT=`cat out/aws_account.txt`


# Create an IAM role - for Lambda
aws iam create-role \
    --role-name $LAMBDA_ROLE \
    --assume-role-policy-document file://role_TrushRelationship.json \
    > out/role.json


# Attach an Inline Policy 
envsubst < DynamoDBWriteAccess_policy.json > out/DynamoDBWriteAccess_policy.json

aws iam put-role-policy \
    --role-name $LAMBDA_ROLE \
    --policy-name $DYNAMODBWRITE_POLICY \
    --policy-document file://out/DynamoDBWriteAccess_policy.json \
    > out/inline_policy.json


# Attach a Managed Policy
aws iam attach-role-policy \
    --role-name $LAMBDA_ROLE \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 

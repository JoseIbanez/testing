#!/bin/bash
set -e

export ROLE_PREFIX="lambda2"


# GET AWS_ACCOUNT
aws sts get-caller-identity --query "Account" --output text > out/aws_account.txt
export AWS_ACCOUNT=`cat out/aws_account.txt`

### Incoming Lambda

# Create an IAM role - for Lambda
aws iam create-role \
    --role-name "${ROLE_PREFIX}_${LAMBDA_INC}" \
    --assume-role-policy-document file://lambda_role_TrushRelationship.json \
    > out/lambda_role_inc.json


# Attach an Inline Policy 
envsubst < lambda_policy_inc.json > out/lambda_policy_inc.json

aws iam put-role-policy \
    --role-name "${ROLE_PREFIX}_${LAMBDA_INC}" \
    --policy-name $LAMBDA_INC \
    --policy-document file://out/lambda_policy_inc.json \
    > out/policy_inc.json


# Attach a Managed Policy
aws iam attach-role-policy \
    --role-name "${ROLE_PREFIX}_${LAMBDA_INC}" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 




### Lambda to Delete files

# Create an IAM role - for Lambda
aws iam create-role \
    --role-name "${ROLE_PREFIX}_${LAMBDA_DEL}" \
    --assume-role-policy-document file://lambda_role_TrushRelationship.json \
    > out/lambda_role_del.json


# Attach an Inline Policy 
envsubst < lambda_policy_del.json > out/lambda_policy_del.json

aws iam put-role-policy \
    --role-name "${ROLE_PREFIX}_${LAMBDA_DEL}" \
    --policy-name $LAMBDA_DEL \
    --policy-document file://out/lambda_policy_del.json \
    > out/policy_del.json


# Attach a Managed Policy
aws iam attach-role-policy \
    --role-name "${ROLE_PREFIX}_${LAMBDA_DEL}" \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 

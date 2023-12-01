#!/bin/bash
set -e


# Lambada Incoming
export ROLE_INC_ARN=`cat out/lambda_role_inc.json | jq -r .Role.Arn`

aws lambda create-function \
    --function-name ${LAMBDA_INC} \
    --runtime python3.8 \
    --zip-file fileb://../lambda_inc/dist/lambda.zip \
    --handler lambda_function.lambda_handler \
    --role ${ROLE_INC_ARN} \
    > out/lambda_function_inc.json


# Lambada Delete
export ROLE_DEL_ARN=`cat out/lambda_role_del.json | jq -r .Role.Arn`

aws lambda create-function \
    --function-name ${LAMBDA_DEL} \
    --runtime python3.8 \
    --zip-file fileb://../lambda_del/dist/lambda.zip \
    --handler lambda_function.lambda_handler \
    --role ${ROLE_DEL_ARN} \
    > out/lambda_function_del.json

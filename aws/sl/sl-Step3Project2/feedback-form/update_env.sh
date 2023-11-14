#!/bin/bash

export LAMBDA_URL=`jq -r '.Stacks[0].Outputs[] | select(.OutputKey == "apiGatewayInvokeURL") | .OutputValue'  ../out/stack.json`

cat env.tpl| envsubst  > .env 

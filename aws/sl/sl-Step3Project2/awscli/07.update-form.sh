#!/bin/bash

export LAMBDA_URL=`jq -r '.Stacks[0].Outputs[] | select(.OutputKey == "apiGatewayInvokeURL") | .OutputValue'  out/stack.json`

# Build js
cd ../feedback-form/
cat env.tpl | envsubst  > .env 
yarn build

# Upload files
cd ../awscli
aws s3 sync ../feedback-form/dist s3://$BUCKETNAME/csb-i36iel/ \
    --exclude '.git/*' 
aws s3 cp ../feedback-form/dist/index.html s3://$BUCKETNAME/

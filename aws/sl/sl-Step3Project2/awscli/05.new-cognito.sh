#!/bin/bash
set -e


export COGNITO_USERPOOL="Feedback"
export WEB_APPLICATION="WebApp"
export POOL_DOMAIN=`echo $BUCKETNAME | tr '[:upper:]' '[:lower:]'`

# Redirect URL
export CF_URL=`cat out/cloudfront.json | jq -r .Distribution.DomainName`
export REDIRECT_URL="https://$CF_URL"
export LOGOUT_URL="https://$CF_URL"

# Create cognito user pool
aws cognito-idp create-user-pool \
    --auto-verified-attributes "email" \
    --username-attributes "email" \
    --username-configuration "CaseSensitive=false" \
    --schema \
    Name=name,Mutable=true,Required=true \
    Name=email,Mutable=true,Required=true \
    Name=phone_number,Mutable=true,Required=true \
    --pool-name $COGNITO_USERPOOL > out/cognito.json

export USERPOOL_ID=`cat out/cognito.json | jq -r .UserPool.Id`


# Add web application
aws cognito-idp create-user-pool-client \
    --user-pool-id $USERPOOL_ID \
    --generate-secret \
    --prevent-user-existence-errors "ENABLED" \
    --client-name $WEB_APPLICATION \
    --explicit-auth-flows "ALLOW_CUSTOM_AUTH" "ALLOW_USER_SRP_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" \
    --supported-identity-providers "COGNITO" \
    --allowed-o-auth-flows-user-pool-client \
    --allowed-o-auth-flows "implicit" \
    --allowed-o-auth-scopes "email" "openid" "profile" \
    --callback-urls $REDIRECT_URL \
    --logout-urls $LOGOUT_URL \
    > out/cognito_client.json


# Configure domain
aws cognito-idp create-user-pool-domain \
    --user-pool-id $USERPOOL_ID \
    --domain $POOL_DOMAIN \
    > out/cognito_domain.json


# Open web page
export CLIENT_ID=`cat out/cognito_client.json | jq -r .UserPoolClient.ClientId`

sleep 5
open -a "Google Chrome" "https://$POOL_DOMAIN.auth.us-east-1.amazoncognito.com/login?client_id=$CLIENT_ID&response_type=token&scope=email+openid&redirect_uri=$REDIRECT_URL"


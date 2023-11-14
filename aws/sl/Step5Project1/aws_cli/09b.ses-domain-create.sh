#!/bin/bash
set -e

# ref:  https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-bring-your-own.html

export PRIVATE_KEY=`cat out/private_str`

envsubst < ses_domain_identity.json > out/ses_domain_identity.json

aws sesv2 create-email-identity \
    --cli-input-json file://out/ses_domain_identity.json


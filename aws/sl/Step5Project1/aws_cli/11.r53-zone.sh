#!/bin/bash

aws route53 create-hosted-zone \
    --name ${MAIL_DOMAIN} \
    --caller-reference 2022-11-0002 \
    --hosted-zone-config Comment="incoming mail" \
    > out/zone.json


export ZONE_ID=`cat out/zone.json | jq -r .HostedZone.Id`
export PUBLIC_KEY=`cat out/public_str`

envsubst < zone_records.json > out/zone_records.json


aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID \
     --change-batch file://out/zone_records.json


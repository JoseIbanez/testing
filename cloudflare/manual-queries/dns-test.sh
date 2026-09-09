#!/bin/bash

export ZONE_ID="your_zone_id_here"
export CLOUDFLARE_API_TOKEN=$(pass cloudflare/DNS_TOKEN)



# Get Zones
curl https://api.cloudflare.com/client/v4/zones \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"

# zone lunes.ovh
export ZONE_ID="c8abe44a1db806687f36b68e97304d45"

# Get DNS Records
curl https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"



# update Manual record

#  "name": "manual1.lunes.ovh",
export DNS_RECORD_ID="4a6b6cf0cf0330062d8a61b65cd4e2c4"

curl https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$DNS_RECORD_ID \
    -X PATCH \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -d '{
        "type": "A",
        "content": "8.8.4.4"
        }'



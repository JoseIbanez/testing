#!/bin/bash

jq_field () {
    echo $ITEM | jq -r ".fields[] | select(.name==\"$1\") | .value"
}


ITEM=$(bw get item "vmanage-aviva.prod")

export VMANAGE_USERNAME=$(echo $ITEM | jq -r '.login.username')
export VMANAGE_PASSWORD=$(echo $ITEM | jq -r '.login.password')
export VMANAGE_URL=$(echo $ITEM | jq -r '.login.uris[0].uri')
export VMANAGE_PROXY=socks5://localhost:9050


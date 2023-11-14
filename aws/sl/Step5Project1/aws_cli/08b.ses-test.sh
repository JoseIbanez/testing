#!/bin/bash
set -e


envsubst < ses_destination.json > out/ses_destination.json


aws ses send-email --from $SENDER_MAIL \
    --destination file://out/ses_destination.json \
    --message file://ses_message.json
#!/bin/bash

aws ec2 import-key-pair \
  --key-name "$AWS_KEY_PAIR_NAME" \
  --public-key-material "fileb://${AWS_KEY_PAIR_FILE}.pub"


aws ec2 request-spot-instances \
  --instance-count 1 \
  --block-duration-minutes 120 \
  --type "one-time" \
  --launch-specification file://specification.json



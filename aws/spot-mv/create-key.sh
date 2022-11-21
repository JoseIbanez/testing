#!/bin/bash

export SSHKEY="SPOT-KEY"

aws ec2 create-key-pair \
   --key-name $SSHKEY \
   --query 'KeyMaterial' --output text > ~/.ssh/$SSHKEY.pem

chmod 700 ~/.ssh/$SSHKEY.pem

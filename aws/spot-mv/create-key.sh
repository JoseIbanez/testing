#!/bin/bash

export SSHKEY="spot-key-02"

aws ec2 create-key-pair \
   --key-name $SSHKEY \
   --query 'KeyMaterial' --output text > ~/.ssh/$SSHKEY.pem

chmod 700 ~/.ssh/$SSHKEY.pem

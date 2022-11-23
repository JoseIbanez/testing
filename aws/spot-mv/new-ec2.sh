#!/bin/bash
set -e

#export AMI="ami-026b57f3c383c2eec"
#export SSHKEY="spot-key"
#export AWS_ZONE="us-east-1a"

export AWS_ZONE="eu-west-1a"
export AMI="ami-026b57f3c383c2eec"
export SSHKEY="spot-key"

###########################
#aws ec2 describe-subnets --query 'Subnets[0]' > out/subnet.json
aws ec2 describe-subnets \
    --query 'Subnets[0]' \
    --filter Name=availability-zone,Values=$AWS_ZONE \
    > out/subnet.json


export VPCID=`jq -r '.VpcId' out/subnet.json`
export SUBNETID=`jq -r '.SubnetId' out/subnet.json`

echo "VPCID: $VPCID"
echo "SUBNETID: $SUBNETID"


###############################


aws ec2 import-key-pair \
  --key-name "$SSHKEY" \
  --public-key-material "fileb://~/.ssh/$SSHKEY.pub"



###############################

aws ec2 run-instances \
    --image-id $AMI \
    --count 1 \
    --instance-market-options '{ "MarketType": "spot" }' \
    --instance-type t2.micro \
    --key-name $SSHKEY \
    --security-group-ids $SG \
    --subnet-id $SUBNETID \
    --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":30,\"DeleteOnTermination\":true}}]" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=bastion}]'  \
    > out/bastion-ec2.json




#!/bin/bash

set -e
###############################

if [ -z "$1" ]; then
    echo "Usage $0 <vmname>"
    exit
fi
export VMNAME=$1


###############################


aws ec2 describe-subnets \
    --query 'Subnets[0]' \
    --filter Name=availability-zone,Values=$AWS_ZONE \
    > out/subnet.json


export VPCID=`jq -r '.VpcId' out/subnet.json`
export SUBNETID=`jq -r '.SubnetId' out/subnet.json`

echo "VPCID: $VPCID"
echo "SUBNETID: $SUBNETID"


##############################

aws ec2 describe-security-groups \
  --filters Name=group-name,Values=default \
  > out/spot-sg.json

export SG=`jq -r '.SecurityGroups[0].GroupId' out/spot-sg.json`
echo "SG: $SG"

echo "VMNAME: $VMNAME"

########################
aws ec2 run-instances \
    --image-id $AMI \
    --count 1 \
    --instance-market-options '{ "MarketType": "spot" }' \
    --instance-type $TSIZE \
    --key-name $SSHKEY \
    --iam-instance-profile "Name=MySessionManagerRole" \
    --security-group-ids $SG \
    --subnet-id $SUBNETID \
    --block-device-mappings "[{\"DeviceName\":\"/dev/sda1\",\"Ebs\":{\"VolumeSize\":30,\"DeleteOnTermination\":true}}]" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$VMNAME}]"  \
    > out/$VMNAME-ec2.json

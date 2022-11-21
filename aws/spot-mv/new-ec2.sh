#!/bin/bash
set -e

export AMI="ami-026b57f3c383c2eec"
export SSHKEY="SPOT-KEY"
export AWS_ZONE="us-east-1a"

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

###########################

aws ec2 create-security-group \
    --group-name bastion-sg \
    --description "Bastion SG" \
    --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=demo-sg}]' \
    --vpc-id $VPCID > out/bastion-sg.json


export SG=`jq -r '.GroupId' out/bastion-sg.json`
echo "SG: $SG"


aws ec2 authorize-security-group-ingress \
    --group-id $SG \
    --tag-specifications 'ResourceType=security-group-rule,Tags=[{Key=Name,Value=demo-sg}]' \
    --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges=[{CidrIp=0.0.0.0/0},{CidrIp=10.0.0.0/24}]" \
    > out/ingress-sg-1.json

aws ec2 authorize-security-group-ingress \
    --group-id $SG \
    --ip-permissions "IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges=[{CidrIp=0.0.0.0/0},{CidrIp=10.0.0.0/24}]" \
    > out/ingress-sg-2.json


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




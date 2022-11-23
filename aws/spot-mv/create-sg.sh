#!/bin/bash



export VPCID=`jq -r '.VpcId' out/subnet.json`

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


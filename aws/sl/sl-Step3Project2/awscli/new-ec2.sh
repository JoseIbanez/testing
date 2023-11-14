#!/bin/bash

AMI="ami-026b57f3c383c2eec"
SSHKEY="sl-vir-01"


###########################
aws ec2 describe-subnets --query 'Subnets[0]' > out/subnet.json

VPCID=`jq -r '.VpcId' out/subnet.json`
SUBNETID=`jq -r '.SubnetId' out/subnet.json`

echo "VPCID: $VPCID"
echo "SUBNETID: $SUBNETID"

###########################

aws ec2 create-security-group \
    --group-name bastion-sg \
    --description "Bastion SG" \
    --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=demo-sg}]' \
    --vpc-id $VPCID > out/bastion-sg.json


SG=`jq -r '.GroupId' out/bastion-sg.json`
echo "SG: $SG"


aws ec2 authorize-security-group-ingress \
    --group-id $SG \
    --tag-specifications 'ResourceType=security-group-rule,Tags=[{Key=Name,Value=demo-sg}]' \
    --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges=[{CidrIp=0.0.0.0/0},{CidrIp=10.0.0.0/24}]" \
    > out/ingress-sg.json

aws ec2 authorize-security-group-ingress \
    --group-id $SG \
    --ip-permissions "IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges=[{CidrIp=0.0.0.0/0},{CidrIp=10.0.0.0/24}]" \
    > out/ingress-sg-2.json


###############################

aws ec2 create-key-pair \
   --key-name $SSHKEY \
   --query 'KeyMaterial' --output text > ~/.ssh/$SSHKEY.pem

chmod 700 ~/.ssh/$SSHKEY.pem

###############################

aws ec2 run-instances \
    --image-id $AMI \
    --count 1 \
    --instance-type t2.micro \
    --key-name $SSHKEY \
    --security-group-ids $SG \
    --subnet-id $SUBNETID \
    --block-device-mappings "[{\"DeviceName\":\"/dev/sdf\",\"Ebs\":{\"VolumeSize\":30,\"DeleteOnTermination\":true}}]" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=bastion}]' 'ResourceType=volume,Tags=[{Key=Name,Value=bastion-disk}]' \
    > out/bastion-ec2.json




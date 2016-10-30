#!/bin/sh

aws ec2 describe-instances | grep -e Spot -e PublicIpAddress -e InstanceType

#!/bin/bash
set -e
aws ec2   describe-spot-instance-requests --query "SpotInstanceRequests[*].[SpotInstanceRequestId, InstanceId, State]" --output table


if [ -z "$1" ]; then
    echo "Usage $0 <request Id>"
    exit
fi

aws ec2 cancel-spot-instance-requests --spot-instance-request-ids $1


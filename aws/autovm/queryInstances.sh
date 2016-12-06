#!/bin/sh

aws ec2 describe-instances | jq '.Reservations[].Instances[] | 
        [{InstanceId: .InstanceId,
          LaunchTime: .LaunchTime, 
          InstanceType: .InstanceType, 
          PublicIpAddres: .PublicIpAddress, 
          SpotInstanceRequestId: .SpotInstanceRequestId}
        ]'

echo ""
echo "V2"
aws ec2 describe-instances | jq '.Reservations[].Instances[] | 
	[{InstanceId: .InstanceId,
          LaunchTime: .LaunchTime,
	  InstanceType: .InstanceType,
	  PublicIpAddres: .PublicIpAddress,
	  SpotInstanceRequestId: .SpotInstanceRequestId, 
	  State: .State.Name, 
          Name: (.Tags[]|select(.Key=="Name")|.Value)
        }]'

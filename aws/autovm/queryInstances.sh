#!/bin/sh

aws ec2 describe-instances  | jq '.Reservations[].Instances[] | 
        [{LaunchTime:.LaunchTime, 
          InstanceType: .InstanceType, 
          PublicIpAddres: .PublicIpAddress, 
          SpotInstanceRequestId: .SpotInstanceRequestId}
        ]'

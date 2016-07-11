#!/bin/sh

cat > ./myVm.json << EOF
{
  "ImageId": "ami-87564feb",
  "KeyName": "kumo",
  "SecurityGroupIds": [ "sg-c5175fac" ],
  "InstanceType": "m3.large"
}
EOF


aws ec2 request-spot-instances \
--spot-price "0.05" \
--instance-count 1 \
--type "one-time" \
--launch-specification file://myVm.json

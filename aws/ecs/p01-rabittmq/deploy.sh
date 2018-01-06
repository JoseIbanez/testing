


aws iam --region us-east-1 create-role --role-name ecsExecutionRole --assume-role-policy-document file://execution-assume-role.json
aws iam --region us-east-1 attach-role-policy --role-name ecsExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

aws logs create-log-group --log-group-name tutorial --region us-east-1
aws logs create-log-group --log-group-name writer   --region us-east-1


ecs-cli configure profile --profile-name ibanez --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY

ecs-cli configure profile --profile-name ibanez


ecs-cli configure \
    --cluster fgw2 \
    --default-launch-type FARGATE \
    --region us-east-1\
    --config-name config1


ecs-cli up



aws ec2 create-security-group --group-name "my-sg" --description "My security group" --vpc-id "VPC_ID"
aws ec2 create-security-group --group-name "my-sg" --description "My security group" --vpc-id "VPC_ID"
aws ec2 authorize-security-group-ingress --group-id "security_group_id" --protocol tcp --port 80 --cidr 0.0.0.0/0


ecs-cli compose --project-name tutorial service up


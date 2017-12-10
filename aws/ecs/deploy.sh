ecs-cli configure profile --profile-name profile_name --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY

ecs-cli configure \
    --cluster fgw2 \
    --default-launch-type FARGATE \
    --region us-east-1\
    --config-name config1


ecs-cli up

aws ec2 create-security-group --group-name "my-sg" --description "My security group" --vpc-id "VPC_ID"

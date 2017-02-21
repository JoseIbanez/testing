#!/bin/bash

source aws.env

aws sns publish \
    --topic-arn arn:aws:sns:eu-west-1:532272748741:Teste \
    --region eu-west-1 \
    --message "Hello World!"


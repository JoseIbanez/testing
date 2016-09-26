#!/bin/bash

declare -x AWS_ACCESS_KEY_ID=`cat  ~/.aws/credentials | grep aws_access_key_id | cut -d ' ' -f 3`
declare -x AWS_SECRET_ACCESS_KEY=`cat  ~/.aws/credentials | grep aws_secret | cut -d ' ' -f 3`


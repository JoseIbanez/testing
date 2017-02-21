#!/bin/sh

source aws.env

stg="$hcs_stg"

echo "Src:" $stg


if [ ! -z $1 ]; then
  gpg -v --passphrase-file ~/.gnupg/testing.pass --output $stg/$1.gpg  -c $stg/$1
fi

if [ ! -z $2 ]; then
  aws s3 sync $stg s3://$aws_bucket/dev01/ --exclude "*" --include "*.gpg"
fi

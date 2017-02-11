#!/bin/sh


if [ ! -z $1 ]; then
  gpg -v --passphrase-file ~/.gnupg/testing.pass --output $1.gpg  -c $1
fi

if [ ! -z $2 ]; then
  aws s3 sync /mnt/tmp/stg/ s3://$aws_bucket/dev01/ --exclude "*" --include "*.gpg"
fi

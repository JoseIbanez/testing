#!/bin/sh

source aws.env

file="hc.sample.tgz"
stg="$HOME/Downloads/"


src="s3://$aws_bucket/dev01/$file.gpg"
echo $src

if [ ! -f $stg/$file.gpg ]; then
  aws s3 cp $src $stg
fi

if [ ! -f $stg/$file ]; then
  gpg --batch --passphrase-file ~/.gnupg/testing.pass --output  $stg/$file -d  $stg/$file.gpg
fi


#tar -xzv -f /tmp/hc.sample.tgz -C $stg

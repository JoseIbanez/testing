#!/bin/sh

file="hc.sample.tgz"
stg="/tmp/stg/"


src="s3://$aws_bucket/dev01/$file.gpg"
echo $src

if [ ! -f /tmp/$file.gpg ]; then
  aws s3 cp $src /tmp/
fi

if [ ! -f /tmp/$file ]; then
  gpg --batch --passphrase-file ~/.gnupg/testing.pass --output /tmp/$file -d /tmp/$file.gpg
fi


#tar -xzv -f /tmp/hc.sample.tgz -C $stg



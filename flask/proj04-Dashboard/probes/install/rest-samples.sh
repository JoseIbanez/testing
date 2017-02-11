#!/bin/sh

source aws.env

file="hc.sample.tgz"

if [ ! -z "$1" ]; then
  file=$1
fi
stg="$hcs_stg"


src="s3://$aws_bucket/dev01/$file.gpg"
echo "Src:" $src
echo "Dst:" $stg

if [ ! -f $stg/$file.gpg ]; then
  aws s3 cp $src $stg
fi

if [ ! -f $stg/$file ]; then
  gpg --batch --passphrase-file ~/.gnupg/testing.pass --output  $stg/$file -d  $stg/$file.gpg
fi


#tar -xzv -f /tmp/hc.sample.tgz -C $stg

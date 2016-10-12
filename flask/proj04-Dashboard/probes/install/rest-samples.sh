#!/bin/sh

stg="/mnt/tmp/stg"


aws s3 cp s3://kumo.fibratel.es/dev01/hc.sample.tgz.gpg /tmp/

gpg --passphrase-file ~/.gnupg/testing.pass --output /tmp/hc.sample.tgz -d /tmp/hc.sample.tgz.gpg

tar -xzv -f /tmp/hc.sample.tgz $stg



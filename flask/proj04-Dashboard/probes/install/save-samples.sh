#!/bin/sh

stg="/mnt/tmp/stg"

tar -czv -f /tmp/hc.sample.tgz $stg
gpg --passphrase-file ~/.gnupg/testing.pass --output /tmp/hc.sample.tgz.gpg  -c /tmp/hc.sample.tgz


aws s3 cp /tmp/hc.sample.tgz.gpg s3://kumo.fibratel.es/dev01/




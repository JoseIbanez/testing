#!/bin/sh

stg="/mnt/tmp/stg"

tar -czv -f /tmp/hc.sample.tgz $stg
gpg --passphrase-file ~/.gnupg/testing.pass --output /tmp/hc.sample.tgz.gpg  -c /tmp/hc.sample.tgz

gpg --passphrase-file ~/.gnupg/testing.pass --output /mnt/tmp/stg/2016-09.tgz.gpg  -c /mnt/tmp/stg/2016-09.tgz
gpg --passphrase-file ~/.gnupg/testing.pass --output /mnt/tmp/stg/2016-08.tgz.gpg  -c /mnt/tmp/stg/2016-08.tgz
gpg --passphrase-file ~/.gnupg/testing.pass --output /mnt/tmp/stg/2016-07.tgz.gpg  -c /mnt/tmp/stg/2016-07.tgz
gpg --passphrase-file ~/.gnupg/testing.pass --output /mnt/tmp/stg/2016-06.tgz.gpg  -c /mnt/tmp/stg/2016-06.tgz



aws s3 cp /tmp/hc.sample.tgz.gpg s3://$aws_bucket/dev01/

aws s3 cp /mnt/tmp/stg/2016-09.tgz.gpg s3://$aws_bucket/dev01/
aws s3 cp /mnt/tmp/stg/2016-08.tgz.gpg s3://$aws_bucket/dev01/
aws s3 cp /mnt/tmp/stg/2016-07.tgz.gpg s3://$aws_bucket/dev01/
aws s3 cp /mnt/tmp/stg/2016-06.tgz.gpg s3://$aws_bucket/dev01/




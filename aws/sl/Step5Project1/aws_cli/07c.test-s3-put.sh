#!/bin/sh

aws s3 ls 

export TARGET=`echo $RANDOM | md5sum | head -c 20; echo;`

aws s3 cp ../requirements/Readme.md s3://$BUCKET_INC/$TARGET.txt

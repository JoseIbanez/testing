#!/bin/bash

docker run --env-file ./var.env  ubuntu bash -c export

docker run --env-file ./var.env  python:2.7-alpine sh -c export

./make.sh
docker images

docker run --env-file ./var.env  boto3 sh -c export

docker run --env-file ./var.env -it  boto3 sh 
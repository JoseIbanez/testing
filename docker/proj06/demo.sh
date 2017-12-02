#!/bin/bash

docker run --env-file ./var.env  ubuntu bash -c export

docker run --env-file ./var.env  python:2.7-alpine sh -c export

./make.sh
docker images

docker tag sqstest $DOCKER_ID_USER/sqstest
docker push $DOCKER_ID_USER/sqstest


docker run --env-file ./var.env  sqstest sh -c export

docker run --env-file ./var.env -it sqstest sh 

docker run -d --env-file ./var.env sqstest /home/producer.py 
docker run -d --env-file ./var.env sqstest /home/receiver.py 

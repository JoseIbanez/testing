#!/bin/bash

export IMG_NAME=job1:dev
export IMG_PUB_NAME=europe-west1-docker.pkg.dev/test-02-e8274/my-docker-repo/job1:dev

export DOCKER_BUILDKIT=1
docker build -f ./Dockerfile . \
        --tag $IMG_NAME 


if [[ "$1" == "publish" ]]; then
        docker tag $IMG_NAME:dev $IMG_PUB_NAME

        gcloud auth print-access-token \
            | docker login \
            -u oauth2accesstoken \
            --password-stdin https://europe-west1-docker.pkg.dev

        echo "Image: $IMG_PUB_NAME"
        docker push  $IMG_PUB_NAME
fi
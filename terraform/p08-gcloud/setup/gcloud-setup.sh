#!/bin/bash

## Configure gcloud to use a SOCKS5 proxy

gcloud config set proxy/type socks5
gcloud config set proxy/address 127.0.0.1
gcloud config set proxy/port 9050



## Docker registry login

gcloud auth print-access-token \
    | docker login \
    -u oauth2accesstoken \
    --password-stdin https://europe-west1-docker.pkg.dev




## Docker tag and push

docker tag busybox:latest europe-west1-docker.pkg.dev/test-02-e8274/my-docker-repo/busybox:dev

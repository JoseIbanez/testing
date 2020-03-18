#!/bin/bash


sudo usermod -aG docker $USER


sudo mkdir -p /jfrog/artifactory
sudo chown -R 1030 /jfrog/

docker kill artifactory
docker rm artifactory

## Enterprise version

docker run  -d -p 8081:8081 -p 8082:8082 \
   --name artifactory \
   -v /jfrog/artifactory:/var/opt/jfrog/artifactory \
   docker.bintray.io/jfrog/artifactory-oss:latest


## CE version

docker run  -d -p 8081:8081 -p 8082:8082 \
   --name artifactory \
   -v /jfrog/artifactory:/var/opt/jfrog/artifactory \
   docker.bintray.io/jfrog/artifactory-cpp-ce

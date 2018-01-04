#debug

docker run -it --add-host "rabbitmq:192.168.1.174" python:2.7-alpine sh
docker run  --add-host "rabbitmq:192.168.1.174" rabbitmq ./mq-write.py

#lauch redis container
docker rm redis
docker run --name redis -d -p 6379:6379 redis:alpine

#create vote image
./make.sh
docker images

#run vote container in interactive mode
docker run -ti -P --link redis:redis vote sh

#lauch vote container
docker run -d -P --link redis:redis vote

export DCK_VERSION=0.1
export DCK_NAME=vote

export DCK_USER=ibanez
docker login

docker tag $DCK_NAME $DCK_USER/$DCK_NAME:$DCK_VERSION
docker tag $DCK_NAME $DCK_USER/$DCK_NAME:latest
docker push $DCK_USER/$DCK_NAME


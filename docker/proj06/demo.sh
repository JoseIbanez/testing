#!/bin/bash

docker run --env-file ./var.env  ubuntu bash -c export

docker run --env-file ./var.env  python:2.7-alpine sh -c export

./make.sh
docker images

docker tag sqstest $DOCKER_ID_USER/sqstest
docker push $DOCKER_ID_USER/sqstest


docker run --env-file ./var.env  sqstest sh -c export

docker run --env-file ./var.env -it ibanez/sqstest sh 

docker run -d --env-file ./var.env sqstest /home/producer.py 
docker run -d --env-file ./var.env sqstest /home/receiver.py 


#swarn

docker swarm init --advertise-addr 172.20.20.11

docker swarm join --token SWMTKN-1-091ggopypyk63wh7ue3stotmse5faz5wikxpeffukp967i3b1g-a1zqb9tw87omf7yds6ykri85j 172.20.20.11:2377

docker service create \
            --mode replicated \
            --replicas 5 \
            --name producer \
            --env-file ./var.env \
            ibanez/sqstest /home/producer.py

docker service ps producer
docker service rm producer


docker service create \
            --mode replicated \
            --replicas 5 \
            --name receiver \
            --env-file ./var.env \
            ibanez/sqstest /home/receiver.py

docker service ps receiver
docker service rm receiver

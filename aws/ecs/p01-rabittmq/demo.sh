
#debug

docker run -it --add-host "rabbitmq:192.168.1.174" python:2.7-alpine sh

docker run  --add-host "rabbitmq:192.168.1.174" rabbitmq ./mq-write.py

./make.sh
docker images

export DOCKER_ID_USER=ibanez
docker login

docker tag rabbitmq $DOCKER_ID_USER/rabbitmq:0.6
docker push $DOCKER_ID_USER/rabbitmq

docker service create \
            --detach \
            --mode replicated \
            --replicas 2 \
            --name producer \
            --host "rabbitmq:192.168.1.174" \
            ibanez/rabbitmq ./mq-write.py

docker service update --image ibanez/rabbitmq:0.2 producer

docker service scale producer=5




52893351-8e7b-46a8-a9a7-3a8b4063a8d9

registry.hub.docker.com/ibanez/rabbitmq:0.2


aws ecr get-login --no-include-email --region us-east-1

docker build -t r1 .

docker tag r1:latest 532272748741.dkr.ecr.us-east-1.amazonaws.com/r1:latest

docker push 532272748741.dkr.ecr.us-east-1.amazonaws.com/r1:latest


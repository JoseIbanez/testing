#!/bin/sh
#######

docker-machine create \
  --driver amazonec2 \
  --engine-install-url https://test.docker.com \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.medium \
  dck-01 &


docker-machine create \
  --driver amazonec2 \
  --engine-install-url https://test.docker.com \
  --amazonec2-vpc-id vpc-608b6f09 \
  --amazonec2-request-spot-instance \
  --amazonec2-spot-price 0.10 \
  --amazonec2-region eu-central-1 \
  --amazonec2-instance-type m3.large \
  dck-01 &



#####

docker swarm init --secret 4wh0m5k61ba8ejezjrccnc3pf \
  --listen-addr 172.31.25.104

docker swarm join --secret 4wh0m5k61ba8ejezjrccnc3pf \
  172.31.25.104:2377

docker node promote dck-02

########
docker network create -d overlay \
    --subnet=172.16.10.0/24 \
    --gateway=172.16.10.1 \
    my-net-01


docker service create --replicas 1 \
    --network my-net-01 \
    --name redis redis:alpine

docker service create --replicas 1 \
    --network my-net-01 \
    --name worker ibanez/worker:1.06

docker service create --mode global \
    --network my-net-01 \
    --name frontend ibanez/frontend:0.01a

docker service create --replicas 1 \
    --network my-net-01 \
    --publish 80:8000/tcp \
    --name fe \
    ibanez/frontend:0.01a


#######

docker service inspect --pretty helloworld
docker service tasks helloworld

docker service scale helloworld=5

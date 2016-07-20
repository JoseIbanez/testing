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
  dck-03 &



#####

docker swarm init --secret 4wh0m5k61ba8ejezjrccnc3pf \
  --listen-addr 172.31.25.100

docker swarm join --secret 4wh0m5k61ba8ejezjrccnc3pf \
  172.31.25.100:2377


########

docker service create --replicas 1 --name helloworld alpine ping docker.com


docker service inspect --pretty helloworld
docker service tasks helloworld

docker service scale helloworld=5

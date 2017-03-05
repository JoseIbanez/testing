#!/bin/sh
name=$1
ip=$2


ssh-add ~/.ssh/kumo.pem
ssh-keygen -R ${name}
ssh-keygen -R ${ip}


scp -r ~/.aws/  ubuntu@${ip}:/home/ubuntu
cat /etc/hosts | grep "${name}$" || echo "${ip}  ${name}" | sudo tee -a /etc/hosts
sudo sed -i'' "s/^.* ${name}$/${ip}   ${name}/g" /etc/hosts

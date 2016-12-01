#!/bin/sh
name=$1
ip=$2

alias kumossh='ssh -i ~/.ssh/kumo.pem'
alias kumoscp='scp -i ~/.ssh/kumo.pem'

scp -i ~/.ssh/kumo.pem -r ~/.aws/  ubuntu@${ip}:/home/ubuntu
cat /etc/hosts | grep "${name}$" || echo "${ip}  ${name}" | sudo tee -a /etc/hosts
sudo sed -i "" "s/^.* ${name}$/${ip}   ${name}/g" /etc/hosts


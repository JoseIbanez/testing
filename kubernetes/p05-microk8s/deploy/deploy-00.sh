#!/bin/bash

sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube

alias kubectl='microk8s.kubectl'

#!/bin/bash

kubectl get node

kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
kubectl get deployments
kubectl get pods

kubectl config view


kubectl expose deployment hello-node --type=LoadBalancer --port=8080
kubectl expose deployment hello-node --port=8080

kubectl get services



kubectl scale deployment/hello-node --replicas=10

kubectl delete service hello-node


wget http://172.28.128.5:8080

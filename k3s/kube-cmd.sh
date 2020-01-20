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





kubectl config set-context --current --namespace=myhello
kubectl create namespace myhello
kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
kubectl get deployments
kubectl get pods
kubectl expose deployment hello-node --type=LoadBalancer --port=8080
kubectl get services
kubectl scale deployment/hello-node --replicas=10



kubectl config set-context --current --namespace=myhello03
kubectl create namespace myhello03

kubectl create deployment hello-node --image=gcr.io/hello-minikube-zero-install/hello-node
kubectl expose deployment hello-node --port=8080
kubectl scale deployment/hello-node --replicas=10


kubectl apply -f redis-sts.yaml
kubectl apply -f redis-svc.yaml


kubectl create deployment nginx --image=nginx
kubectl apply -f nginx-svc.yaml
kubectl scale deployment/nginx --replicas=5


kubectl get deployments
kubectl get statefulset
kubectl get pods
kubectl get services


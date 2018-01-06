

kubectl run redis --image=redis:alpine --port 6379
kubectl expose deployment redis --type=NodePort
kubectl expose deployment redis --type=ClusterIP


kubectl run vote --image=ibanez/vote:latest --port 8000
kubectl expose deployment vote --type=NodePort
kubectl expose deployment vote --type=LoadBalancer
kubectl scale deployment/vote --replicas 5

kubectl get pods

kubectl describe deployment redis
kubectl describe deployment vote

kubectl delete service    vote
kubectl delete deployment vote

kubectl delete service    redis
kubectl delete deployment redis

kubectl set image deployment/vote vote=ibanez/vote:0.2

kubectl rollout status deployment vote

kubectl scale deployment/vote --replicas 5
kubectl get pod

for i in {0..100}; do ./c02.py -host 192.168.99.100 -port 30108 ; done




declare -x http_proxy=http://10.74.42.22:8080
declare -x https_proxy=https://10.74.42.22:8080


minikube \
   --docker-env="http_proxy=http://10.74.42.22:8080" \
   --docker-env="https_proxy=https://10.74.42.22:8080" \
   start

kubectl config use-context minikube
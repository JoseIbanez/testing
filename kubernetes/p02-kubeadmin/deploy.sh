
https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/

#docker CE
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

add-apt-repository \
   "deb https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"

apt-get update && apt-get install -y docker-ce=$(apt-cache madison docker-ce | grep 17.03 | head -1 | awk '{print $3}')

#kubeadm

apt-get update && apt-get install -y apt-transport-https

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF

apt-get update
apt-get install -y kubelet kubeadm kubectl

#For master
kubeadm init --pod-network-cidr=192.168.0.0/16

export KUBECONFIG=/etc/kubernetes/admin.conf


#master runs containers 
kubectl taint nodes --all node-role.kubernetes.io/master-

#network calico
sysctl net.bridge.bridge-nf-call-iptables=1
kubectl apply -f https://docs.projectcalico.org/v2.6/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml

#network weave net
export kubever=$(kubectl version | base64 | tr -d '\n')
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$kubever"

#check
kubectl get deployments --all-namespaces
kubectl get nodes

#On slaves
kubeadm join --token 0276fc.cb48d4e9e175e45e 172.31.23.171:6443 --discovery-token-ca-cert-hash sha256:92a80e5ecbfbac76585c1370174074b4159d03aa3ec99c5192ab7272db5bf367
kubeadm join --token d97f15.5075f6765416735b 172.31.26.217:6443 --discovery-token-ca-cert-hash sha256:aa709f42c2b6725c0b3c04c16a9ee4acaaa3466d3a5b7c878eaa611f50a1ba46

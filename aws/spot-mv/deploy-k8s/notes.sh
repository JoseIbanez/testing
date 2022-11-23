# Swap off ?
sudo swapoff -a


# Download

wget --user=LFtraining --password=Penguin2014 \
    https://training.linuxfoundation.org/cm/LFD259/LFD259_V2022-11-23_SOLUTIONS.tar.xz 

tar -xvf LFD259_V2022-11-23_SOLUTIONS.tar.xz 


cp LFD259/SOLUTIONS/s_02/k8sWorker.sh .


kubeadm join 172.30.0.21:6443 --token jexgu5.0c6rxr8otpi47vhe \
        --discovery-token-ca-cert-hash sha256:48b96ebadbe1b3e965ba80e57c24c6de3d826a895fed257ec627bc4f4ab1c92b 

sudo apt-get install bash-completion vim -y


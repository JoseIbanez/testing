

sudo systemctl stop apparmor
sudo systemctl disable apparmor
sudo systemctl status apparmor


# Download
wget --user=LFtraining --password=Penguin2014 \
    https://training.linuxfoundation.org/cm/LFD259/LFD259_V2022-11-23_SOLUTIONS.tar.xz 

tar -xvf LFD259_V2022-11-23_SOLUTIONS.tar.xz 

####################
# Control Plane node
####################
cp LFD259/SOLUTIONS/s_02/k8scp.sh .
bash k8scp.sh | tee $HOME/cp.out

# Short cuts
alias k="kubectl"
export do="--dry-run=client -o yaml"
export force="--force --grace-period=0"

# Auto completion BASH
sudo apt-get install bash-completion vim -y
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> $HOME/.bashrc

# Auto completion ZSH
autoload -Uz compinit
compinit
source <(kubectl completion zsh)


####################
# Worker node
####################

cp LFD259/SOLUTIONS/s_02/k8sWorker.sh .






kubeadm join 172.30.0.21:6443 --token jexgu5.0c6rxr8otpi47vhe \
        --discovery-token-ca-cert-hash sha256:48b96ebadbe1b3e965ba80e57c24c6de3d826a895fed257ec627bc4f4ab1c92b 

sudo apt-get install bash-completion vim -y


#############
https://github.com/containerd/containerd/issues/6009


sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

grep SystemdCgroup /etc/containerd/config.toml 
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml


sudo systemctl restart containerd
sudo systemctl restart kubelet

kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

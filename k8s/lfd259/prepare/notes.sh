

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



# Add load to control panel node
kubectl describe nodes | grep -i taint
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl describe nodes | grep -i taint






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



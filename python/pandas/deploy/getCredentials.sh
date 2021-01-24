#!/bin/bash

sudo apt install lastpass-cli

mkdir -p $HOME/.secrets
mkdir -p $HOME/.config
mkdir -p $HOME/.local/share

lpass login
lpass show --notes ibanez-001-8e1126c08504.json > $HOME/.secrets/ibanez-001-8e1126c08504.json 
cat $HOME/.secrets/ibanez-001-8e1126c08504.json 

lpass logout

mkdir -p $HOME/.secrets/

cat <<EOF >> $HOME/.bashrc
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.secrets/ibanez-001-8e1126c08504.json"
EOF

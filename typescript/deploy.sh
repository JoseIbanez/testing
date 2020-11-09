#!/bin/bash

# https://linuxize.com/post/how-to-install-node-js-on-ubuntu-18.04/

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.36.0/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm --version

nvm install node
node --version

npm install -g typescript
npm install -g ts-node

tsc -v


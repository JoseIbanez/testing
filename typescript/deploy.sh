#!/bin/bash

# https://linuxize.com/post/how-to-install-node-js-on-ubuntu-18.04/


#Install nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
nvm --version

#Install nodejs
nvm install node
node --version

#Install typescript
npm install -g typescript
tsc --version



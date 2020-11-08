#!/bin/bash

# https://linuxize.com/post/how-to-install-node-js-on-ubuntu-18.04/

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.36.0/install.sh | bash
nvm --version

nvm install node
node --version

npm install -g typescript
tsc -v



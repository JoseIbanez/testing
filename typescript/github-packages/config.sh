#!/bin/bash



npm login --scope=@OWNER --registry=https://npm.pkg.github.com


cat << EOF > ~/.npmrc
//npm.pkg.github.com/:_authToken=$GHTOKEN
@OWNER:registry=https://npm.pkg.github.com/
EOF


npm set registry "https://npm.pkg.github.com/jibanezvela"
npm set //npm.pkg.github.com/:_authToken $GHTOKEN

cat ~/.npmrc 


#!/bin/bash
set -e

openssl genrsa -f4 -out out/private.key 1024
openssl rsa -in out/private.key -outform PEM -pubout -out out/public.key


cat out/private.key | ggrep -v -E '\--' |  tr -d '\n' > out/private_str
cat out/public.key  | ggrep -v -E '\--' |  tr -d '\n' > out/public_str


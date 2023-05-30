#!/bin/bash

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365

# non-interactive and 10 years expiration

export FILENAME=grpc.example.com.crt
export SUBJ="/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=h3.local"
openssl req -x509 -newkey rsa:4096 -keyout $FILENAME.key -out $FILENAME.crt -sha256 -days 3650 -nodes -subj $SUBJ

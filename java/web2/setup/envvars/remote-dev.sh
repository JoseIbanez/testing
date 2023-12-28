#!/bin/bash

export POSTGRES_PASSWORD=$(pass develop/postgres/POSTGRES_PASSWORD)
export POSTGRES_USERNAME=$(pass develop/postgres/POSTGRES_USERNAME)
export POSTGRES_DB=demo


export ES_URL="https://a396d3dc7d7846c59f186b53b7eca133.eu-west-1.aws.found.io:9243"
export ES_USERNAME=$(pass prod/ES_USERNAME)
export ES_PASSWORD=$(pass prod/ES_PASSWORD)

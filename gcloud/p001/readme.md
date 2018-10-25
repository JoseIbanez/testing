# Project gcloud p001: niceTag


## Run local debug

    dev_appserver.py app.yaml 

## Post a new value

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"my.tag003", "name":"ver","value":"1.1.1"}' \
  http://localhost:8080/build

## Get image

    GET  http://localhost:8080/build?id=my.tag003


## Upload app

    gcloud app deploy


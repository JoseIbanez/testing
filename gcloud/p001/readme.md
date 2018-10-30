# Project gcloud p001: niceTag


## Run local debug

    dev_appserver.py app.yaml 

## Post a new value

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"my.tag001", "name":"ver","value":"1.1.1"}' \
  http://localhost:8080/build
```



## Get image
![tag](http://p001.com.com.es/build?id=my.tag001)

    GET  http://p001.com.com.es/build?id=my.tag001



## Upload app

    gcloud app deploy


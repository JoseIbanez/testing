#!/bin/bash

curl -X POST "$ES_URL/rn*syslog*/_search?size=10000" \
--user "$ES_USERNAME:$ES_PASSWORD" \
-H 'Content-Type: application/json' -d'
{
  "query": {
    "bool":{
      "must_not": {
         "terms": {
            "message": [ "times","sshd", "sendmsg" ]
         }
      }
    }
  },
  "fields": [
    "message",
    "device_name",
    "tenant_name",
    "syslog_timestamp",
    "syslog-timestamp"
  ],
  "_source": false
}
' > out.json

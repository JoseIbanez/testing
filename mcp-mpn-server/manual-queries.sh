
export ES_URL=https://esm-development.es.eu-west-1.aws.found.io:9243
export ES_USERNAME=`pass develop/ES_USERNAME`
export ES_PASSWORD=`pass develop/ES_PASSWORD`

export ES_URL=https://beceea2874d94e448c312e0450bde5fc.eu-west-1.aws.found.io:9243
export ES_USERNAME=`pass preprod/ES_USERNAME`
export ES_PASSWORD=`pass preprod/ES_PASSWORD`



INDEX="esm-mpn-logstash-mpn-status-engine"

curl -k -H "Content-Type: application/json" \
--user "$ES_USERNAME:$ES_PASSWORD" \
"$ES_URL/$INDEX*/_search" -d"$QUERY" | jq .



QUERY=$(cat <<-END
{"query":
  {"range":
    {"@timestamp": 
      {"gte": "2025-03-01T00:00:00.000Z"}
    }
  },
  "_source": false
}
END
)


QUERY=$(cat <<-END

{
  "_source": false,
  "size": 20,
  "fields": ["@timestamp", "eventTime","customer", "metric.*", "metric.soruce.id"],
  "query": {
    "bool": {
      "filter": [
        {
          "range": { "@timestamp": { "gte": "2025-03-01" } }
        },
        {
          "match": {  "metric.name": "rag_number" }
        },
        {
          "match": {  "source.labels.resource_type": "network" }
        }
      ]
    }
  },
  "collapse": {
    "field": "customer.keyword"
  },
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ]
}
END
)





GET test/_search
{
  "_source": false,
  "query": {
    "match_all": {}
  },
  "collapse": {
    "field": "customer",
    "inner_hits": [
      {
        "name": "latest",      
        "size": 1,
        "sort": [
          {
            "date": {
              "order": "desc"
            }
          }
        ]
      }
    ]
  }
}
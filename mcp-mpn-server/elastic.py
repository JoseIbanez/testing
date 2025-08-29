import os
import json
import logging
from elasticsearch import Elasticsearch
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)



def get_credentials() -> tuple[str,str]:

    credentials_file = "~/.config/mcp/elastic_mpn"
    fullfilename = os.path.expanduser(credentials_file)
    try:
        with open(fullfilename,encoding="utf-8") as file:
            elasticSecret = json.load(file)
            es_username = elasticSecret.get('username')
            es_password = elasticSecret.get('password')

    except OSError as e:
        raise Exception(f"Unable to load elastic secret file:{credentials_file}") from e
 
    return es_username,es_password


@cached(cache=TTLCache(ttl=60, maxsize=100))
def get_es_customer_list():

    es_url = os.environ.get("ES_URL")
    es_username,es_password = get_credentials()

    if not es_url:
        raise ValueError("Environment variables ES_URL must be set.")

    index="esm-mpn-logstash-mpn-status-engine"

    body = {
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


    es = Elasticsearch(es_url,http_auth=(es_username,es_password),
            timeout=30, max_retries=1, retry_on_timeout=True,
            verify_certs=True)

    resp = es.search(index=index,           ## pylint: disable=unexpected-keyword-arg
                body=body,
                size=20)


    return resp


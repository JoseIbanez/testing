
import json
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)


def get_customer_list(dict) -> list[dict]:

    hits = dict.get("hits", {}).get("hits", [])

    customer_list = []
    for hit in hits:
        source = hit.get("_source", {})

            
        customer_state ={
            "name": source.get("customer"),
            "last_report": source.get("eventTime"),
            "network_state": source.get("metric", {}).get("labels", {}).get("rag","UNKNOWN"),
        }
        logger.info(f"Customer: {customer_state['name']} - Last Report: {customer_state['last_report']} - State: {customer_state['network_state']}")

        customer_list.append(customer_state)

    return customer_list


def custumer_details(dict, customer) -> dict:
    """
    Returns a dictionary with customer details.
    """
    hits = dict.get("hits", {}).get("hits", [])

    customer_state = {}
    for hit in hits:
        source = hit.get("_source", {})
        customer_name = source.get("customer", "")
        if customer_name != customer:
            continue

        labels = source.get("metric", {}).get("labels", {})

        ap_red = labels.get("ap_red", [])
        ap_amber = labels.get("ap_amber", [])
        ap_green = labels.get("ap_green", [])
        ap_unknown = labels.get("ap_unknown", [])

        cs_red = labels.get("cs_red", [])
        cs_amber = labels.get("cs_amber", [])
        cs_green = labels.get("cs_green", [])
        cs_unknown = labels.get("cs_unknown", [])

        error_list = labels.get("error_code", [])

        customer_state ={
            "name": source.get("customer"),
            "last_report": source.get("eventTime"),
            "network_state": labels.get("rag","UNKNOWN"),
            "error_list": error_list,

            "total_access_points": len(ap_red) + len(ap_amber) + len(ap_green) + len(ap_unknown),
            "access_points_red_state": ap_red,
            "access_points_amber_state": ap_amber,
            "access_points_green_state": ap_green,
            "access_points_unknown_state": ap_unknown,

            "total_core_servers": len(cs_red) + len(cs_amber) + len(cs_green) + len(cs_unknown),
            "core_servers_red_state": cs_red,
            "core_servers_amber_state": cs_amber,
            "core_servers_green_state": cs_green,
            "core_servers_unknown_state": cs_unknown,
        }
        logger.info(f"Customer: {customer_state['name']} - Last Report: {customer_state['last_report']} - State: {customer_state['network_state']}")


    return customer_state

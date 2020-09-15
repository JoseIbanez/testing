#!/usr/bin/python3.7

#https://www.mydataschool.com/tutDatawarehouseBigQuery-2.html
#https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries#client-libraries-install-python

import json
import logging
import os
import traceback
from datetime import datetime
import io
import re
import sys
#from six import StringIO
#from six import BytesIO

from google.api_core import retry
from google.cloud import bigquery
# from google.cloud import firestore
# from google.cloud import pubsub_v1
#from google.cloud import storage


PROJECT_ID = 'ibanez-001'
BQ_DATASET = 'covid19_es'
BQ_TABLE = 'cases'
#CS = storage.Client()
BQ = bigquery.Client()
job_config = bigquery.LoadJobConfig()

def delete_rows_by_index(index):
    query = f"""
            DELETE
            FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}`
            WHERE index = {index}
            """
    query_job = BQ.query(query)
    results = query_job.result()  # Waits for job to complete.


def insert_rows_into_bigquery(rows, row_ids):
     #blob = CS.get_bucket(bucket_name).blob(file_name)
     #row = json.loads(blob.download_as_string())
     print('rows: ', rows)
     table = BQ.dataset(BQ_DATASET).table(BQ_TABLE)
     errors = BQ.insert_rows_json(table,
                                   json_rows=rows,
                                   row_ids=row_ids,
                                   retry=retry.Retry(deadline=30))

     print(errors)
     if errors != []:
          raise BigQueryError(errors)

     return "ok"

def insert_table(rows):

     row_ids = []
     for item in rows:
          row_ids.append(item["id"])


     #delete_rows_by_index(205)
     ret = insert_rows_into_bigquery(rows, row_ids)

     return ret



if __name__ == "__main__":

     #rows = [
     #     {"date": "2020-10-01",
     #      "index": 205,
     #      "region_iso":"CLM"},
     #     {"date": "2020-10-01",
     #      "index": 205,
     #      "region_iso":"ES"},
     #]
     #row_ids = ["205.CM", "205.ES"]

     index=sys.argv[1]


     with open(f"./data/task-{index}.cases.format.json", "r") as f:
          rows=json.loads(f.read())

     row_ids = []
     for item in rows:
          row_ids.append(item["id"])


     #delete_rows_by_index(205)
     ret = insert_rows_into_bigquery(rows, row_ids)


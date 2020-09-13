#!/usr/bin/python3.7

from google.cloud import bigquery

PROJECT_ID = 'ibanez-001'
BQ_DATASET = 'covid19ES_dev'


def query_stackoverflow():
    client = bigquery.Client()
    #query_job = client.query(
    #    """
    #    SELECT
    #      CONCAT(
    #        'https://stackoverflow.com/questions/',
    #        CAST(id as STRING)) as url,
    #      view_count
    #    FROM `bigquery-public-data.stackoverflow.posts_questions`
    #    WHERE tags like '%google-bigquery%'
    #    ORDER BY view_count DESC
    #    LIMIT 10"""
    #)

    query = """
            SELECT *
            FROM `ibanez-001.covid19ES_dev.cases`
            LIMIT 100
            """
    query_job = client.query(query)

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.date, row.index))

if __name__ == "__main__":
    query_stackoverflow()

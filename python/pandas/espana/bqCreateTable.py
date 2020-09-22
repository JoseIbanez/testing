#!/usr/bin/python3


from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

PROJECT_ID = 'ibanez-001'
BQ_DATASET = 'covid19_es'


def createCasesTable():

    BQ_TABLE = 'cases'

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    schema = [
        bigquery.SchemaField("id",          "STRING", mode="REQUIRED"),
        bigquery.SchemaField("date",        "DATE" ),
        bigquery.SchemaField("index",       "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("region_iso",  "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region_name", "STRING" ),
        bigquery.SchemaField("cases_total", "INTEGER" ),
        bigquery.SchemaField("cases_1day",  "INTEGER" ),

        bigquery.SchemaField("cases_14d",     "INTEGER" ),
        bigquery.SchemaField("cases_14d_ai",  "FLOAT" ),

        bigquery.SchemaField("cases_7d",      "INTEGER" ),
        bigquery.SchemaField("cases_7d_ai",   "FLOAT" ),

        bigquery.SchemaField("symptoms_14d",    "INTEGER" ),
        bigquery.SchemaField("symptoms_14d_ai", "FLOAT" ),

        bigquery.SchemaField("symptoms_7d",     "INTEGER" ),
        bigquery.SchemaField("symptoms_7d_ai",  "FLOAT" )
    ]


    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )



def createHospitalTable():

    BQ_TABLE = 'hospital'

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    schema = [
        bigquery.SchemaField("id",          "STRING", mode="REQUIRED"),
        bigquery.SchemaField("date",        "DATE" ),
        bigquery.SchemaField("index",       "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("region_iso",  "STRING", mode="REQUIRED"),
        bigquery.SchemaField("region_name", "STRING" ),

        bigquery.SchemaField("hospital_total", "INTEGER" ),
        bigquery.SchemaField("hospital_7d",    "INTEGER" ),

        bigquery.SchemaField("icu_total",      "INTEGER" ),
        bigquery.SchemaField("icu_7d",         "INTEGER" ),

        bigquery.SchemaField("death_total",    "INTEGER" ),
        bigquery.SchemaField("death_7d",       "INTEGER" )
    ]


    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

if __name__ == '__main__':
    createHospitalTable()



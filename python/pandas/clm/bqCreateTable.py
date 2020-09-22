#!/usr/bin/python3


from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

PROJECT_ID = 'ibanez-001'
BQ_DATASET = 'covid19_es'


def createCasesTable():

    BQ_TABLE = 'cases_CLM'

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    schema = [
        bigquery.SchemaField("id",          "STRING", mode="REQUIRED"),
        bigquery.SchemaField("date",        "DATE" ),
        bigquery.SchemaField("region_iso",  "STRING"),
        bigquery.SchemaField("region_name", "STRING" ),

        bigquery.SchemaField("cases_total", "INTEGER" ),
        bigquery.SchemaField("cases_1d",     "INTEGER" ),

        bigquery.SchemaField("hospital_current", "INTEGER" ),

        bigquery.SchemaField("icu_current",      "INTEGER" ),

        bigquery.SchemaField("death_total",      "INTEGER" ),
        bigquery.SchemaField("death_1d",         "INTEGER" )

    ]


    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )




if __name__ == '__main__':
    #createHospitalTable()
    createCasesTable()


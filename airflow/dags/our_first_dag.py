from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

defult_args = {
    'owner': 'coder2',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}



with DAG(
    dag_id='our_first_dag',
    schedule='@daily',
    default_args=defult_args,
    description='A simple DAG to demonstrate Airflow setup',
    start_date= datetime(2025, 6, 1)
) as dag:
    task1 = BashOperator(
        task_id='print_date',
        bash_command='date; echo " for {{ds}} "',
    )

    task1


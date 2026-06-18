from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, '/opt/airflow')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.transform_datafr import transform_and_save_all

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="transformation_silver_dag",
    default_args=default_args,
    description='Pipeline pour la transformation des donnees de la Bronze -> Silver',
    start_date=datetime(2026, 6, 1),
    schedule_interval=None, # On le lance manuellement ou via un autre DAG
    catchup=False
) as dag:

    # Tâche unique : scanne Bronze et transforme vers Silver
    task1 = PythonOperator(
        task_id='run_transformation_silver',
        python_callable=transform_and_save_all
    )
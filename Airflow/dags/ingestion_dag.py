from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ajout du chemin pour trouver ton dossier 'scripts'
sys.path.insert(0, '/opt/airflow')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.recup_france_travail import run_collecte

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="ingestion_dags",
    default_args=default_args,
    description='Ingestion des donnees (Zone Bronze)',
    start_date=datetime(2026, 6, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='run_france_travail_collecte',
        python_callable=run_collecte,
    )
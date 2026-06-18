from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
import sys
import os
# sys.path.insert(0, '/opt/airflow')
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from scripts.recup_france_travail import run_collecte
# from scripts.load_to_postgres import load_silver_to_gold
# from scripts.vectorisateur_data import vectorize_missing_offers

default_args = {
    'owner': 'Fidelia',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
    
with DAG(
    dag_id='master_pipeline_full_workflow',
    default_args=default_args,
    description='Chef orchestre pour déclencher les autres dans le bon ordre',
    start_date=datetime(2026, 6, 18),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # 1. Scrapping
    trigger_scrapping = TriggerDagRunOperator(
        task_id='trigger_scrapping',
        trigger_dag_id='scrapping_france_travail' # ID de ton DAG actuel
    )

    # 2. Ingestion (Silver -> Gold)
    trigger_ingestion = TriggerDagRunOperator(
        task_id='trigger_ingestion',
        trigger_dag_id='load_silver_to_gold'
    )

    # 3. Enrichissement (Vectorisation)
    trigger_vectorization = TriggerDagRunOperator(
        task_id='trigger_vectorization',
        trigger_dag_id='vectorize_offres'
    )

    # L'ordre logique
    trigger_scrapping >> trigger_ingestion >> trigger_vectorization
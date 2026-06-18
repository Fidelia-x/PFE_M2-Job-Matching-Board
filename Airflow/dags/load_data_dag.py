from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, '/opt/airflow')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.load_to_postgres import load_silver_to_gold
from scripts.vectorisateur_data import vectorize_missing_offers

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=2),
    'start_date': datetime(2026, 6, 1),
}

with DAG(
    dag_id="dag_load_to_gold",
    default_args=default_args,
    description='Chargement des donnees de la Silver -> Gold (Postgres) + calcul des vecteurs pour chaque offres',
    start_date=datetime(2026, 6, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id='load_silver_to_postgres',
        python_callable=load_silver_to_gold
    )

    task_vectorize = PythonOperator(
        task_id='vectorize_offres',
        python_callable=vectorize_missing_offers
    )

    # Définition de la dépendance (La flèche magique)
    load_task >> task_vectorize
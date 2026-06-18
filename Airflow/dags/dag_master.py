from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import sys
import os

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
        trigger_dag_id='ingestion_dags',
        wait_for_completion=True,  # ✅ attend la fin du DAG
        poke_interval=30,           # vérifie toutes les 30s
        allowed_states=['success'], # échoue si le DAG cible échoue
    )

    # 2. Ingestion (Silver -> Gold)
    trigger_ingestion = TriggerDagRunOperator(
        task_id='trigger_ingestion',
        trigger_dag_id='transformation_silver_dag',
        wait_for_completion=True,
        poke_interval=30,
        allowed_states=['success'],
    )

    # 3. Vectorisation
    trigger_vectorization = TriggerDagRunOperator(
        task_id='trigger_load_silver_to_gold_and_vectorisation',
        trigger_dag_id='dag_load_to_gold',
        wait_for_completion=True,
        poke_interval=30,
        allowed_states=['success'],
    )

    create_index_task = PostgresOperator(
    task_id='create_vector_index',
    postgres_conn_id='postgres_default', # Ton ID de connexion Postgres
    sql="""
        CREATE INDEX IF NOT EXISTS idx_offres_embedding 
        ON offres_emploi 
        USING hnsw (embedding vector_cosine_ops);
    """
    )

    # L'ordre logique
    trigger_scrapping >> trigger_ingestion >> trigger_vectorization >> create_index_task
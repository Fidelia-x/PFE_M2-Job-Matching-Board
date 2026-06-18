import pandas as pd
import json
import re
from minio import Minio
import pyarrow as pa
import pyarrow.parquet as pq
import io
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

CONN_ID  = "minio"

def extract_salary(salary_data):
    """Extrait min et max depuis le dictionnaire ou la chaîne de salaire."""
    if not isinstance(salary_data, dict):
        return 0.0, 0.0
    
    # On récupère le texte, soit via 'libelle', soit via 'commentaire'
    text = salary_data.get('libelle') or salary_data.get('commentaire', "")
    
    # Regex pour trouver les nombres (ex: 22404.2)
    numbers = [float(s) for s in re.findall(r'\d+\.?\d*', str(text))]
    
    if len(numbers) >= 2:
        return numbers[0], numbers[1]
    elif len(numbers) == 1:
        return numbers[0], numbers[0]
    return 0.0, 0.0

def transformer_data(json_data):
    df = pd.DataFrame(json_data.get('offres', []))
    df_clean = pd.DataFrame()
    
    # Mapping complet
    df_clean['id_france_travail'] = df['id']
    df_clean['titre'] = df['intitule']
    df_clean['description'] = df['description']
    # Gestion des tableaux (ARRAY dans Postgres)
    df_clean['competences'] = df['competences'].apply(lambda x: [item['libelle'] for item in x] if isinstance(x, list) else [])
    df_clean['languages'] = df['langues'].apply(lambda x: [item['libelle'] for item in x] if isinstance(x, list) else [])
    
    df_clean['contract'] = df['typeContratLibelle']
    df_clean['diplome_requis'] = df['qualificationLibelle']
    df_clean['education'] = df['formations'].apply(lambda x: x[0].get('niveauLibelle') if isinstance(x, list) and len(x) > 0 else None)
    df_clean['localisation'] = df['lieuTravail'].apply(lambda x: x.get('libelle') if isinstance(x, dict) else None)
    
    # Salaires
    salaires = df['salaire'].apply(extract_salary)
    df_clean['salaire_min'] = [s[0] for s in salaires]
    df_clean['salaire_max'] = [s[1] for s in salaires]
    
    df_clean['experience_years'] = df['experienceExige'].map({'D': 0, 'E': 3}).fillna(1)
    df_clean['source_url'] = df['origineOffre'].apply(lambda x: x.get('urlOrigine') if isinstance(x, dict) else None)
    df_clean['source_platform'] = 'France Travail'
    df_clean['company'] = df['entreprise'].apply(lambda x: x.get('nom', 'N/A') if isinstance(x, dict) else 'N/A')
    df_clean['date_du_poste'] = pd.to_datetime(df['dateCreation'])
    
    return df_clean

def save_to_silver(df, minio_client, bucket_name, object_name):
    # Conversion du DataFrame en format Parquet dans un buffer mémoire
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    
    # Upload vers MinIO
    minio_client.put_object(
        bucket_name,
        object_name,
        data=buffer,
        length=buffer.getbuffer().nbytes
    )
    print(f"✅ Fichier sauvegardé dans silver : {object_name}")

def transform_and_save_all():
    hook = S3Hook(aws_conn_id=CONN_ID)
    
    # 1. Lister tous les fichiers dans bronze
    keys = hook.list_keys(bucket_name="bronze", prefix="france_travail/")
    
    if not keys:
        print("Aucun fichier trouvé dans bronze/france_travail/")
        return

    for key in keys:
        # Définir le chemin de destination (silver)
        silver_path = key.replace("bronze/", "silver/").replace(".json", ".parquet")
        
        # 2. VÉRIFICATION : Le fichier existe-t-il déjà dans Silver ?
        if hook.check_for_key(key=silver_path, bucket_name="silver"):
            print(f"⏩ Déjà traité : {silver_path}, on passe.")
            continue
            
        print(f"🔄 Transformation de {key}...")
        
        # 3. Télécharger, transformer et sauvegarder
        obj = hook.get_key(key, bucket_name="bronze")
        data = json.loads(obj.get()['Body'].read().decode('utf-8'))
        
        df = transformer_data(data) # Ta fonction de transfo existante
        
        # Sauvegarde en Parquet via le hook
        # Note: on utilise un buffer pour créer le parquet en mémoire
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        hook.load_bytes(
            bytes_data=buffer.getvalue(),
            key=silver_path,
            bucket_name="silver",
            replace=True
        )
        print(f"✅ Fichier sauvegardé : {silver_path}")
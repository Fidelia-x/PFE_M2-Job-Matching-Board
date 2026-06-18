import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import io
from psycopg2.extras import execute_values
import numpy as np
import re

CONN_ID  = "minio"

def init_database(pg_hook):
    """Vérifie si les tables existent, sinon les crée."""
    sql_create = """
    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS offres_emploi (
        id_offres_emploi SERIAL PRIMARY KEY,
        id_france_travail VARCHAR(50) UNIQUE,
        titre VARCHAR(255),
        description TEXT,
        competences TEXT[],
        languages TEXT[],
        contract TEXT,
        diplome_requis TEXT,
        education TEXT,
        localisation TEXT,
        salaire_min FLOAT,
        salaire_max FLOAT,
        experience_years INTEGER,
        source_url TEXT,
        source_platform TEXT,
        company TEXT NOT NULL,
        date_du_poste TIMESTAMP,
        embedding vector(384)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_source_url ON offres_emploi (source_url);
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_id_ft ON offres_emploi (id_france_travail);
    """
    pg_hook.run(sql_create)

def format_array(x):
    # Si c'est un tableau numpy ou une liste
    if isinstance(x, (list, np.ndarray)) and len(x) > 0:
        # Convertit en liste python si c'est un ndarray
        data = x.tolist() if isinstance(x, np.ndarray) else x
        # Ajoute les guillemets nécessaires pour Postgres : {"A","B"}
        return "{" + ",".join(f'"{str(item)}"' for item in data) + "}"
    
    # Si c'est vide, on renvoie une chaîne vide pour un tableau Postgres vide
    return "{}"

def clean_languages(description):
    text = str(description).lower()
    found_langs = []
    
    # Dictionnaire : mot-clé détecté -> Nom affiché proprement
    languages_map = {
        'english': 'English', 'anglais': 'English',
        'french': 'Français', 'français': 'Français', 'francais': 'Français',
        'german': 'Allemand', 'allemand': 'Allemand',
        'spanish': 'Espagnol', 'espagnol': 'Espagnol',
        'chinese': 'Chinois', 'mandarin': 'Chinois'
    }
    
    for key, value in languages_map.items():
        if key in text and value not in found_langs:
            found_langs.append(value)
            
    return found_langs if found_langs else []

def clean_competences(description):
    # 1. On convertit tout le texte en minuscules une seule fois
    text = str(description).lower()
    
    # 2. On définit tes listes de compétences, toujours en minuscules
    categories = {
    'Langages pour le Backend': ['python', 'java', 'scala', 'go', 'node.js', 'fastapi', 'flask', 'r'],
    'Langages pour le Frontend': ['javascript', 'typescript', 'react', 'vue', 'html', 'css', 'angular', 'Svelte'],

    'Data Stores': ['postgresql', 'mongodb', 'mysql', 'redis', 'elasticsearch', 'snowflake', 'oracle'],

    'Cloud & Infra': ['sql', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'snowflake', 'terraform'],
    'Data Engineering': ['dbt', 'airflow', 'spark', 'kafka', 'hadoop'],
    'IA/ML': ['tensorflow', 'pytorch', 'scikit-learn', 'llm', 'rag', 'mlops', 'langchain'],
    'No-Code': ['airtable', 'make', 'bubble', 'power bi', 'zapier', 'tableau', 'metabase', 'webflow', 'excel', 'notion']
    }
    
    found_skills = []
    
    # 3. La comparaison se fait maintenant sur deux minuscules
    for category, skills in categories.items():
        for skill in skills:
            if skill in text: # 'skill' est déjà en minuscule ici
                found_skills.append(skill.capitalize()) # On remet la majuscule juste pour l'affichage propre
                
    return list(set(found_skills)) # set() évite les doublons si le mot apparaît deux fois

def clean_education_level(text):
    text = str(text).lower()
    
    # On définit des mots-clés qui caractérisent un niveau
    if any(m in text for m in ['bac+5', 'master', 'ingénieur', 'école d\'ingénieur', 'm2']):
        return 'Bac+5 / Ingénieur'
    elif any(m in text for m in ['bac+3', 'licence', 'bachelor', 'l3']):
        return 'Bac+3 / Bachelor'
    elif any(m in text for m in ['doctorat', 'phd']):
        return 'Doctorat'
    else:
        return 'Non précisé'

# def clean_company(name):
#     if not name or pd.isna(name):
#         return "Non précisée"
    
#     # 1. On enlève les espaces inutiles au début et à la fin
#     name = str(name).strip()
    
#     # 2. On met le nom en format "Title Case" pour que ça soit propre
#     # (ex: "SNCF" reste "SNCF", "google" devient "Google")
#     return name.title() if len(name) > 4 else name.upper()

# def load_silver_to_gold():
#     hook = S3Hook(aws_conn_id=CONN_ID)
#     # 2. Connexion Postgres (pour écrire dans la base)
#     pg_hook = PostgresHook(postgres_conn_id="postgres_default")
#     init_database(pg_hook)

#     # Lister les fichiers Parquet dans Silver
#     keys = hook.list_keys(bucket_name="silver", prefix="france_travail/")
    
#     for key in keys:
#         # Lire le Parquet
#         obj = hook.get_key(key, bucket_name="silver")
#         df = pd.read_parquet(io.BytesIO(obj.get()['Body'].read()))

#         df['competences'] = df['competences'].apply(format_array)
#         df['languages'] = df['languages'].apply(format_array)
        
#         # Assure-toi que les valeurs NaN ne bloquent pas
#         df = df.where(pd.notnull(df), None)

#         # Préparer les données pour l'insertion
#         # Note: on utilise 'execute_values' pour aller très vite
#         rows = df.values.tolist()
        
#         insert_query = """
#             INSERT INTO offres_emploi (
#                 titre, description, competences, languages, contract, 
#                 diplome_requis, education, localisation, salaire_min, 
#                 salaire_max, experience_years, source_url, source_platform, 
#                 company, date_du_poste
#             ) VALUES %s
#             ON CONFLICT (source_url) DO NOTHING;
#         """
        
#         # pg_hook.insert_rows est plus simple, mais execute_values est plus rapide
#         # Ici on utilise une méthode simple compatible avec le hook
#         pg_hook.insert_rows(
#             table="offres_emploi",
#             rows=rows,
#             target_fields=[
#                 'titre', 'description', 'competences', 'languages', 'contract', 'diplome_requis', 'education', 'localisation', 'salaire_min',
#                 'salaire_max','experience_years', 'source_url', 'source_platform', 'company', 'date_du_poste'
#             ]
#         )
#         print(f"✅ Données de {key} chargées dans la table 'offres_emploi'")

def load_silver_to_gold():
    hook = S3Hook(aws_conn_id=CONN_ID)
    pg_hook = PostgresHook(postgres_conn_id="postgres_default")
    init_database(pg_hook)

    keys = hook.list_keys(bucket_name="silver", prefix="france_travail/")

    if not keys:
        print("⚠️ Aucun fichier trouvé dans silver/france_travail/")
        return
    
    for key in keys:
        print(f"📂 Traitement de : {key}")
        obj = hook.get_key(key, bucket_name="silver")
        df = pd.read_parquet(io.BytesIO(obj.get()['Body'].read()))

        print("DEBUG: Aperçu des données lues :")
        print(df[['competences', 'languages']].head(2))
        # DEBUG : Vérifie si ce ne sont pas des chaînes de caractères au lieu de listes
        print(f"Type de la colonne competences : {type(df['competences'].iloc[0])}")

        df = df.drop_duplicates(subset=['source_url'], keep='last')

        print(f"DEBUG: Colonnes disponibles dans le fichier : {df.columns.tolist()}")

        # Nettoyage des données
        df['competences'] = df['description'].apply(clean_competences)
        df['competences'] = df['competences'].apply(format_array)

        df['languages'] = df['description'].apply(clean_languages)
        df['languages'] = df['languages'].apply(format_array)

        # df['company'] = df['company'].apply(clean_company)
        df['diplome_requis'] = df['education']
        df['education'] = df['diplome_requis'].apply(clean_education_level)
        
        df['experience_years'] = df['experience_years'].fillna(1).astype(int)

        df = df.where(pd.notnull(df), None)

        
        # Requête SQL avec Upsert
        upsert_sql = """
        INSERT INTO offres_emploi (
            id_france_travail, titre, description, competences, languages, 
            contract, diplome_requis, education, localisation, salaire_min, 
            salaire_max, experience_years, source_url, source_platform, company, date_du_poste, embedding
        ) VALUES %s
        ON CONFLICT (source_url) 
        DO UPDATE SET 
            titre = EXCLUDED.titre,
            description = EXCLUDED.description,
            salaire_min = EXCLUDED.salaire_min,
            salaire_max = EXCLUDED.salaire_max,
            competences  = EXCLUDED.competences;
        """
            # embedding = EXCLUDED.embedding;

        # Exécution de l'Upsert ligne par ligne
        # En Python, l'underscore est une convention pour dire : "Je sais que cette valeur existe, 
        # mais je ne vais pas l'utiliser". Ici, iterrows() renvoie toujours deux choses (l'index et la ligne). 
        # Comme tu n'as pas besoin du numéro de la ligne (l'index) pour faire ton insertion, tu le stockes dans _ pour dire "ignore-le".
        
        # for _, row in df.iterrows():
        #     params = (
        #         row['id_france_travail'], row['titre'], row['description'], 
        #         row['competences'], row['languages'], row['contract'], 
        #         row['diplome_requis'], row['education'], row['localisation'], 
        #         row['salaire_min'], row['salaire_max'], row['experience_years'], 
        #         row['source_url'], row['source_platform'], row['company']
        #         # row['embedding']
        #     )

        #     pg_hook.run(upsert_sql, parameters=params)
            
        # print(f"✅ Données de {key} chargées avec succès (Upsert appliqué)")

    # Prépare les tuples pour execute_values (beaucoup plus rapide)
        rows = [
            (
                row['id_france_travail'],
                row['titre'],
                row['description'],
                row['competences'],
                row['languages'],
                row['contract'],
                row['diplome_requis'],
                row['education'],
                row['localisation'],
                row['salaire_min'],
                row['salaire_max'],
                row['experience_years'],
                row['source_url'],
                row['source_platform'],
                row['company'],
                row['date_du_poste'],
                None  # embedding — sera rempli en S5
            )
            for _, row in df.iterrows()
        ]

        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        execute_values(cursor, upsert_sql, rows)
        conn.commit()
        cursor.close()
        print(f"✅ {len(rows)} offres chargées depuis {key}")


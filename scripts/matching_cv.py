import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
import os

# Configuration (à adapter selon tes variables d'environnement)
DB_CONFIG = {
    "dbname": "job_matching",
    "user": "user",
    "password": "password",
    "host": "localhost",
    # "host": "postgres",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def find_best_matches(cv_text, top_n=3):
    # 1. Chargement du modèle (lazy loading : uniquement quand on appelle la fonction)
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # 2. Vectorisation du CV
    cv_vector = model.encode(cv_text).tolist()
    
    # 3. Connexion à la base et Matching
    conn = get_db_connection()
    register_vector(conn) # Indispensable pour pgvector
    cur = conn.cursor()
    
    sql_query = """
    SELECT id_france_travail, titre, company, 
           1 - (embedding <=> %s::vector) AS similarity_score
    FROM offres_emploi
    WHERE date_du_poste >= NOW() - INTERVAL '30 days'
      AND embedding IS NOT NULL
    ORDER BY similarity_score DESC
    LIMIT %s;
    """
    
    cur.execute(sql_query, (str(cv_vector), top_n))
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Retourner une liste de dictionnaires plus facile à manipuler
    return [
        {"id": r[0], "titre": r[1], "company": r[2], "score": round(r[3], 3)} 
        for r in results
    ]


# from mistralai.client import MistralClient

# def analyze_gap(cv_text, job_description):
#     client = MistralClient(api_key="TA_CLE_API_MISTRAL")
    
#     prompt = f"""
#     Analyse ce CV et cette offre d'emploi.
#     CV: {cv_text}
#     Offre: {job_description}
    
#     Réponds sous ce format JSON strict :
#     {{
#         "competences_manquantes": ["comp1", "comp2"],
#         "conseil": "Texte court",
#         "projet_suggere": "Nom d'un projet pour apprendre ces skills"
#     }}
#     """
    
#     response = client.chat(model="mistral-medium", messages=[{"role": "user", "content": prompt}])
#     return response.choices[0].message.content
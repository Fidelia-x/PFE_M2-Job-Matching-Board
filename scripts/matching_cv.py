import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
import os

from scripts.skills_reference import extract_skills

# Configuration (à adapter selon tes variables d'environnement)
DB_CONFIG = {
    "dbname": "job_matching",
    "user": "user",
    "password": "password",
    # "host": "localhost",
    "host": "postgres",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Le modèle est chargé une seule fois par process (il pèse plusieurs centaines
# de Mo) et réutilisé à chaque appel, plutôt que rechargé à chaque matching.
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _model

def _encode_cv(cv_text):
    model = get_model()
    return model.encode(cv_text).tolist()


def find_best_matches(cv_text, top_n=3):
    # 1. Vectorisation du CV
    cv_vector = _encode_cv(cv_text)

    # 2. Compétences détectées dans le CV (même référentiel que les offres, voir
    # scripts.skills_reference), pour pouvoir comparer avec les compétences
    # requises par chaque offre.
    cv_skills = set(extract_skills(cv_text))

    # 3. Connexion à la base et Matching
    conn = get_db_connection()
    register_vector(conn) # Indispensable pour pgvector
    cur = conn.cursor()

    sql_query = """
    SELECT id_france_travail, titre, company, localisation, contract,
           salaire_min, salaire_max, source_url, competences,
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
    matches = []
    for r in results:
        offer_skills = r[8] or []
        matched_skills = [s for s in offer_skills if s in cv_skills]
        missing_skills = [s for s in offer_skills if s not in cv_skills]
        matches.append({
            "id": r[0],
            "titre": r[1],
            "company": r[2],
            "localisation": r[3],
            "contract": r[4],
            "salaire_min": r[5],
            "salaire_max": r[6],
            "source_url": r[7],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "score": round(r[9], 3),
        })
    return matches


def get_market_fit_stats(cv_text, eligibility_threshold=0.70):
    """Statistiques du CV face à l'ensemble du marché (même fenêtre de 30
    jours que find_best_matches), pas seulement le top_n affiché à l'écran :
    - eligibility_rate : % des offres où le score dépasse eligibility_threshold
    - avg_similarity : similarité moyenne sur toute la fenêtre (calculée sur
      la totalité plutôt que sur le seul top_n, sinon la moyenne serait
      artificiellement tirée vers 1 par les meilleurs résultats)
    Agrégé côté SQL (COUNT/AVG) plutôt qu'en rapatriant chaque ligne, pour
    éviter de transférer tout le texte/les colonnes inutiles ici."""
    cv_vector = _encode_cv(cv_text)

    conn = get_db_connection()
    register_vector(conn)
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                COUNT(*),
                COUNT(*) FILTER (WHERE 1 - (embedding <=> %s::vector) > %s),
                AVG(1 - (embedding <=> %s::vector))
            FROM offres_emploi
            WHERE date_du_poste >= NOW() - INTERVAL '30 days'
              AND embedding IS NOT NULL
        """, (str(cv_vector), eligibility_threshold, str(cv_vector)))
        total, eligible, avg_similarity = cur.fetchone()
        cur.close()
    finally:
        conn.close()

    if not total:
        return {"total": 0, "eligible": 0, "eligibility_rate": 0, "avg_similarity": 0.0}
    return {
        "total": total,
        "eligible": eligible,
        "eligibility_rate": round(100 * eligible / total),
        "avg_similarity": round(float(avg_similarity), 3) if avg_similarity is not None else 0.0,
    }


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
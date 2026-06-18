import psycopg2
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_values

conn_params = "dbname=job_matching host=postgres user=user password=password"

def vectorize_missing_offers():
    conn = psycopg2.connect(conn_params)
    cur = conn.cursor()
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # On ne récupère que les offres qui n'ont pas encore d'embedding
    cur.execute("SELECT id_offres_emploi, description FROM offres_emploi WHERE embedding IS NULL")
    rows = cur.fetchall()
    
    if not rows:
        print("Toutes les offres sont déjà vectorisées.")
        return

    print(f"Vectorisation de {len(rows)} offres...")

    descriptions = [row[1] for row in rows] # row[1] est la description
    embeddings = model.encode(descriptions, batch_size=32, show_progress_bar=True)

    updates = []

    for i in range(len(rows)):
        # On convertit le vecteur numpy en liste python ici même
        vector_python = embeddings[i].tolist() 
        updates.append((vector_python, rows[i][0]))
    
    # 4. Insertion en masse
    update_sql = """
    UPDATE offres_emploi AS t
    SET embedding = data.embedding::vector
    FROM (VALUES %s) AS data(embedding, id_offres_emploi)
    WHERE t.id_offres_emploi = data.id_offres_emploi
    """
    
    execute_values(cur, update_sql, updates)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Vectorisation terminée.")

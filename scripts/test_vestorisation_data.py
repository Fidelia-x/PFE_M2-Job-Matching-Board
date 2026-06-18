from sentence_transformers import SentenceTransformer
import psycopg2

# 1. Charger le modèle
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. Connexion (utilise tes variables d'environnement ici)
# conn = psycopg2.connect(dbname="ta_base", user="ton_user", password="ton_password")
conn = psycopg2.connect(dbname="job_matching", user="user", password="password")
cur = conn.cursor()

# 3. Récupérer UNE seule ligne pour le test
cur.execute("SELECT id_offres_emploi, description FROM offres_emploi LIMIT 1")
offre = cur.fetchone()

if offre:
    id_offre, desc = offre
    print(f"Description trouvée : {desc[:50]}...")
    
    # 4. Calculer le vecteur
    vecteur = model.encode(desc).tolist()
    print(f"Dimension du vecteur calculé : {len(vecteur)}")
    
    # 5. Tenter l'insertion
    cur.execute("UPDATE offres_emploi SET embedding = %s WHERE id_offres_emploi = %s", (vecteur, id_offre))
    conn.commit()
    print("✅ Test réussi : La ligne a bien été mise à jour dans PostgreSQL.")
else:
    print("❌ Aucune offre trouvée dans la table.")

cur.close()
conn.close()
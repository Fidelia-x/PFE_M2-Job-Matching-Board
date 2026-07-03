import psycopg2
import bcrypt
from scripts.matching_cv import get_db_connection

# DB_CONFIG = {
#     "dbname": "job_matching",
#     "user": "user",
#     "password": "password",
#     "host": "localhost",
#     # "host": "postgres",
#     "port": "5432"
# }

# def get_db_connection():
#     return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Initialise la base de données : crée la table users si elle n'existe pas."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Création de la table users avec sécurité
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,         
        nom VARCHAR(100),
        prenom VARCHAR(100),
        email VARCHAR(150) UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'candidat',        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Base de données initialisée avec succès.")

import psycopg2
from scripts.matching_cv import get_db_connection

def init_db():
    """Initialise la base de données : crée la table users si elle n'existe pas."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Création de la table users avec sécurité
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users ( 
        username VARCHAR(50) PRIMARY KEY,
        password_hash VARCHAR(255) NOT NULL,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        numero_telephone VARCHAR(20),
        email VARCHAR(150) UNIQUE,
        pays VARCHAR(100),
        role VARCHAR(20) DEFAULT 'user'        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Base de données initialisée avec succès.")

# Appelle cette fonction au démarrage de ton application
init_db()
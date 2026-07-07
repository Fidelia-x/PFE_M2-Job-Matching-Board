import bcrypt
import psycopg2

import sys
import os
sys.path.append('/scripts')

from scripts.matching_cv import get_db_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def register_user(nom, prenom, email, password):
    hashed = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (nom, prenom, email, password_hash) VALUES (%s, %s, %s, %s)",
            (nom, prenom, email, hashed)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur : {e}")
        return False
    finally:
        cur.close()
        conn.close()

def verify_user(email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    # On récupère l'id et le hash pour vérifier
    cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    result = cur.fetchone()
    conn.close()
    
    if result and check_password(password, result[1]):
        return result[0] # Retourne l'ID si succès
    return None
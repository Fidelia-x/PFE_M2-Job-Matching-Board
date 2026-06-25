import bcrypt
import psycopg2

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def verify_user(username, password):
    # Connexion à ta BDD (utilise ta fonction de connexion existante)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    conn.close()
    
    if result and check_password(password, result[0]):
        return True
    return False
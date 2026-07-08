import re
import bcrypt
import psycopg2
from scripts.matching_cv import get_db_connection

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def is_valid_email(email: str) -> bool:
    """Vérifie que l'email a un format valide (syntaxe uniquement)."""
    return re.match(EMAIL_REGEX, email) is not None


def normalize_email(email: str) -> str:
    """Normalise l'email (minuscules, espaces retirés) pour éviter les doublons."""
    return email.strip().lower()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def register_user(nom: str, prenom: str, email: str, password: str):
    """
    Crée un utilisateur.

    Retourne un tuple (user_id, message) :
      - (id, "ok")                  si succès
      - (None, "email_invalide")    si le format de l'email est incorrect
      - (None, "email_deja_utilise") si l'email existe déjà
      - (None, "erreur_serveur")    en cas d'erreur inattendue (DB, etc.)
    """
    if not is_valid_email(email):
        return None, "email_invalide"

    email = normalize_email(email)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Vérification explicite d'unicité AVANT insertion
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return None, "email_deja_utilise"

        hashed = hash_password(password)
        cur.execute(
            """INSERT INTO users (nom, prenom, email, password_hash)
               VALUES (%s, %s, %s, %s)
               RETURNING id""",
            (nom, prenom, email, hashed)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id, "ok"

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de l'inscription : {e}")
        return None, "erreur_serveur"

    finally:
        cur.close()
        conn.close()


def verify_user(email: str, password: str):
    """
    Vérifie les identifiants d'un utilisateur.

    Retourne un tuple (user_id, message) :
      - (id, "ok")                    si succès
      - (None, "email_invalide")      si le format de l'email est incorrect
      - (None, "identifiants_invalides") si email ou mot de passe incorrect
      - (None, "erreur_serveur")      en cas d'erreur inattendue (DB, etc.)
    """
    if not is_valid_email(email):
        return None, "email_invalide"

    email = normalize_email(email)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        result = cur.fetchone()

        if result and check_password(password, result[1]):
            return result[0], "ok"

        return None, "identifiants_invalides"

    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        return None, "erreur_serveur"

    finally:
        cur.close()
        conn.close()

def get_user_info(user_id: int):
    """Récupère nom et prénom d'un utilisateur à partir de son ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nom, prenom FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        if result:
            return {"nom": result[0], "prenom": result[1]}
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {e}")
        return None
    finally:
        cur.close()
        conn.close()
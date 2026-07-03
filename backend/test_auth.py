# test_auth.py
# from auth_service import register_user
from backend.auth_service import register_user
# from gestion_table_user import init_db
from backend.gestion_table_user import init_db


# 1. Tester l'initialisation
init_db()

# 2. Tester l'inscription
succes = register_user("Nono", "SISI", "nono@example.com", "mon_super_password")
if succes:
    print("Inscription OK !")
else:
    print("Erreur inscription.")

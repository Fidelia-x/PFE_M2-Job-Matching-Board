"""Backfill ponctuel de offres_emploi.secteur_activite pour les offres déjà en
base : le champ vient d'être ajouté au pipeline (transform_datafr.py), mais
les ~8000 offres existantes ont été chargées avant. Comme le JSON brut de
chaque offre est déjà conservé dans MinIO (bronze/france_travail/*.json), on
peut remplir la colonne sans repasser par l'API France Travail — on relit
juste les fichiers déjà collectés et on met à jour par id_france_travail.

Usage : python scripts/backfill_secteur_activite.py
(à exécuter une fois, depuis la machine hôte — utilise les ports exposés par
docker-compose : postgres:5432, minio:9000)
"""
import io
import json
import os
import sys
import psycopg2

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
from minio import Minio
from psycopg2.extras import execute_values

PG_CONFIG = {
    "dbname": os.environ.get("POSTGRES_DB", "job_matching"),
    "user": os.environ.get("POSTGRES_USER", "user"),
    "password": os.environ.get("POSTGRES_PASSWORD", "password"),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", "5432"),
}

MINIO_CONFIG = {
    "endpoint": os.environ.get("MINIO_ENDPOINT", "localhost:9000"),
    "access_key": os.environ.get("MINIO_USER", "minioadmin"),
    "secret_key": os.environ.get("MINIO_PASSWORD", "minio_password"),
    "secure": False,
}


def collect_sector_by_offer_id(minio_client):
    """Parcourt tous les fichiers bronze et retourne {id_france_travail: secteur_activite}."""
    sectors = {}
    objects = minio_client.list_objects("bronze", prefix="france_travail/", recursive=True)
    n_files = 0
    for obj in objects:
        if not obj.object_name.endswith(".json"):
            continue
        n_files += 1
        resp = minio_client.get_object("bronze", obj.object_name)
        try:
            payload = json.loads(resp.read().decode("utf-8"))
        finally:
            resp.close()
            resp.release_conn()

        for offre in payload.get("offres", []):
            offer_id = offre.get("id")
            secteur = offre.get("secteurActiviteLibelle")
            if offer_id and secteur:
                sectors[offer_id] = secteur

    print(f"{n_files} fichiers bronze lus, {len(sectors)} secteurs identifiés")
    return sectors


def apply_backfill(sectors):
    conn = psycopg2.connect(**PG_CONFIG)
    try:
        cur = conn.cursor()
        rows = list(sectors.items())
        # page_size >= len(rows) : une seule requête UPDATE, sinon execute_values
        # découpe en pages de 100 par défaut et cur.rowcount ne refléterait que
        # la dernière page au lieu du total.
        execute_values(
            cur,
            """
            UPDATE offres_emploi AS o
            SET secteur_activite = v.secteur
            FROM (VALUES %s) AS v(id_france_travail, secteur)
            WHERE o.id_france_travail = v.id_france_travail
            """,
            rows,
            page_size=len(rows),
        )
        updated = cur.rowcount
        conn.commit()
        cur.close()
        print(f"{updated} offres mises à jour avec leur secteur d'activité")
    finally:
        conn.close()


def main():
    minio_client = Minio(**MINIO_CONFIG)
    sectors = collect_sector_by_offer_id(minio_client)
    if not sectors:
        print("⚠️ Aucun secteur trouvé dans les fichiers bronze, rien à faire.")
        return
    apply_backfill(sectors)


if __name__ == "__main__":
    main()

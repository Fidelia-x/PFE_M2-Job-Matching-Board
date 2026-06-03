#code 1
# identifiant client: PAR_jobmatching_0079a623d606e91e9dd17dd8c6ebdc3a3cf6ba0a4dd308c99a920b872339732e
# cle secrete: c7b10462ffffb3ba58d73cc7386716988370e7c6652b6c307ccce76ab85eb89d

#code 2
# identifiant client:PAR_jobmatching_ca23ea217d4adb9ecf93e3e6553e9971a37ae7d9109fce006e6937246246395c
# cle secrete:3fbdcd7be2387dc8aba83f0d899438c0d61d3794a4f140d34e2b47acb8d49640

import os
import json
import requests
from minio import Minio
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

load_dotenv()

CONN_ID  = "minio"

# jobs à collecter
JOBS = [
    "data engineer",
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "MLOps",
    "développeur python"
]

API_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

#authentification
def get_access_token():
    """Récupère le token OAuth2 auprès de France Travail."""
    client_id = Variable.get("CLIENT_ID")
    client_secret = Variable.get("CLIENT_SECRET")

    print(f"DEBUG: CLIENT_ID récupéré via Airflow = {client_id}")

    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    response = requests.post(url, data=data)

    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code}: {response.text}")
        
    response.raise_for_status()
    token_data = response.json()
    print(f"✅ Token valide pour {token_data.get('expires_in', '?')} secondes")
    return token_data['access_token']


# COLLECTE AVEC PAGINATION(page)
def recup_all_pages(headers, job):
    """
    Récupère toutes les pages de résultats pour un métier donné.
    FranceTravail renvoie max 150 offres par requête — on pagine automatiquement.
    Toute la France — pas de filtre géographique.
    """
    all_offres = []
    start = 0
    page_size = 149

    while True:
        params = {
            "motsCles": job,
            "range":    f"{start}-{start + page_size}"
        }

        response = requests.get(API_URL, headers=headers, params=params)

        # 206 = résultats partiels (pagination), 200 = dernière page
        if response.status_code in [200, 206]:
            data     = response.json()
            offres   = data.get("resultats", [])
            all_offres.extend(offres)
            print(f"   Page {start // 150 + 1} : {len(offres)} offres récupérées")

            # Moins de 150 résultats → on est sur la dernière page
            if len(offres) < page_size:
                break

            start += page_size

        else:
            print(f"❌ Erreur {response.status_code} pour : {job}")
            break

    return all_offres

# STOCKAGE MINIO S3Hook

def fichier_existe(hook, bucket, filename):
    try:
        hook.check_for_key(key=filename, bucket_name=bucket)
        return True
    except Exception as e:
        if "403" in str(e) or "Forbidden" in str(e):
            raise
        return False

def upload_to_minio(bucket, filename, offres, metadata):
    """Upload les offres JSON dans MinIO via S3Hook."""
    hook = S3Hook(aws_conn_id=CONN_ID)

    payload = {
        "metadata":  metadata,
        "nb_offres": len(offres),
        "offres":    offres
    }
    data_str = json.dumps(payload, ensure_ascii=False)
    print(f"🚀 Upload direct en mémoire de {filename} dans le bucket '{bucket}'...")

    hook.load_string(
        string_data = data_str,
        key         = filename,
        bucket_name = bucket,
        replace     = True
    )
    print(f"✅ Uploadé : {filename} ({len(offres)} offres stockées)")
    return True

# RAPPORT DE COLLECTE

def generer_rapport(stats, date):
    """Génère un rapport JSON dans bronze/rapports/."""
    hook    = S3Hook(aws_conn_id=CONN_ID)
    rapport = {
        "date":         date,
        "source":       "france_travail",
        "total_offres": sum(s["nb_offres"] for s in stats),
        "detail":       stats
    }

    hook.load_string(
        string_data = json.dumps(rapport, ensure_ascii=False),
        key         = f"rapports/france_travail_{date}.json",
        bucket_name = "bronze",
        replace     = True
    )

    print(f"\n{'='*50}")
    print(f"📊 Collecte terminée — {rapport['total_offres']} offres au total")
    print(f"📁 Rapport : bronze/rapports/france_travail_{date}.json")
    print(f"{'='*50}")


def main():
    print("🚀 Démarrage de la collecte France Travail...\n")

    # 2. Récupérer le token OAuth2
    token   = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    date    = datetime.now().strftime("%Y%m%d_%H%M")
    stats   = []

    # 3. Collecter chaque métier
    for job in JOBS:
        print(f"\n🔍 Collecte : {job}")

        offres = recup_all_pages(headers, job)

        if offres:
            filename = f"france_travail/{job.replace(' ', '_')}_{date}.json"

            upload_to_minio(
                bucket   = "bronze",
                filename = filename,
                offres   = offres,
                metadata = {
                    "source":       "france_travail",
                    "job":          job,
                    "date_collecte": date,
                }
            )

            stats.append({
                "job":       job,
                "nb_offres": len(offres),
                "fichier":   filename
            })
        else:
            print(f"⚠️  Aucune offre trouvée pour : {job}")

    # 4. Générer le rapport
    generer_rapport(stats, date)


# if __name__ == "__main__":
#     main()

def run_collecte():
    """Fonction appelée par Airflow"""
    main()

if __name__ == "__main__":
    run_collecte()
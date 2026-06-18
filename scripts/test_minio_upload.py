import os
import json
from minio import Minio
from dotenv import load_dotenv
from io import BytesIO

# 1. Chargement des configs
load_dotenv()

def upload_to_minio(data, filename):
    client = Minio(
        "localhost:9000", # Dans docker-compose, on utilise le nom du service
        access_key=os.getenv("MINIO_USER"),
        secret_key=os.getenv("MINIO_PASSWORD"),
        secure=False
    )

    # Convertir les données en format binaire pour MinIO
    data_bytes = json.dumps(data).encode('utf-8')
    data_stream = BytesIO(data_bytes)

    # 2. Upload dans le bucket 'bronze'
    client.put_object(
        "bronze",
        filename,
        data_stream,
        length=len(data_bytes),
        content_type="application/json"
    )
    print(f"Fichier {filename} envoyé avec succès dans le bucket bronze.")

if __name__ == "__main__":
    # Simulation d'une réponse d'API
    data_to_store = {"job": "Data Engineer", "status": "active", "source": "FranceTravail"}
    upload_to_minio(data_to_store, "jobs_data_2026_06_01.json")
# generate_data/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM apache/airflow:2.8.0
RUN pip install minio requests python-dotenv
RUN pip install sentence-transformers
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# Copier le code FastAPI
COPY . .

# Lancer FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
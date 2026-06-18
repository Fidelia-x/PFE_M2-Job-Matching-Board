import json
from transform_datafr import transformer_data

# 1. Simule un fichier JSON (celui que tu as récupéré de MinIO)
with open('data_analyst_20260603_1337.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Lance la fonction
df_result = transformer_data(data)

# 3. Vérifie le résultat
print(df_result.head())
print(df_result.columns)
import pandas as pd

df = pd.read_parquet("data_analyst_20260603_1337.parquet")
print(df.head())
print(df.columns)
print(df.info()) # Très important : vérifie que les salaires sont en 'float' et les dates en 'datetime'
import pandas as pd

df = pd.read_parquet(
    "data/processed/clean_laps/hungary_2025_clean.parquet"
)

print(df.columns.tolist())
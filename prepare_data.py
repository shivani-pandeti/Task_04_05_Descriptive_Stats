"""
prepare_data.py
Filters the raw box office CSV down to a clean, working subset: 2021-2024.
Run once to produce movies_2021_2024_clean.csv
"""

import pandas as pd

RAW_PATH = "enhanced_box_office_data(2000-2024)u.csv"
OUT_PATH = "movies_2021_2024_clean.csv"

df = pd.read_csv(RAW_PATH)

# 1. Keep only 2021, 2022, 2023, 2024
df = df[df["Year"].isin([2021, 2022, 2023, 2024])].copy()

# 2. Clean the Rating column: "6.126/10" -> 6.126 (a real float we can do math on)
df["Rating_clean"] = df["Rating"].str.split("/").str[0].astype(float)

# 3. Sanity checks - eyeball these before trusting the output
print("Shape:", df.shape)
print(df["Year"].value_counts())
print("Missing values per column:")
print(df.isnull().sum())

# 4. Save the clean subset
df.to_csv(OUT_PATH, index=False)
print(f"Saved clean subset to {OUT_PATH}")
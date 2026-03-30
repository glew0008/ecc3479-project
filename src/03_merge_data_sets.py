import pandas as pd
import os

# --- Ensure script runs from project root ---
# This makes the script work even if it's inside "code/" or "src/"
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

# --- Load cleaned datasets ---
df_2016 = pd.read_csv("data/clean/2016_census_clean.csv")
df_2021 = pd.read_csv("data/clean/2021_census_clean.csv")

# --- Add year column if missing ---
if "year" not in df_2016.columns:
    df_2016["year"] = 2016

if "year" not in df_2021.columns:
    df_2021["year"] = 2021

# --- Ensure consistent column order ---
cols = ["year", "income_bracket", "education", "count"]
df_2016 = df_2016[cols]
df_2021 = df_2021[cols]

# --- Merge datasets ---
df_all = pd.concat([df_2016, df_2021], ignore_index=True)

# --- Save merged dataset ---
output_path = "data/clean/merged_2016_2021.csv"
df_all.to_csv(output_path, index=False)

print(f"Merged dataset saved to {output_path}")
print(df_all.head())

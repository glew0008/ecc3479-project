"""
clean_data.py

This script reads the raw unemployment dataset, performs basic cleaning,
creates additional variables, and saves a cleaned version to data/clean/.
It does not overwrite the raw file.
"""

import pandas as pd

# 1. Read raw data
df = pd.read_csv("data/raw/sample_data.csv")

# 2. Rename unclear variables (example)
df = df.rename(columns={
    "unemployment_rate": "unemp_rate",
    "participation_rate": "part_rate"
})

# 3. Create quarter_num (convert Q1–Q4 to 1–4)
df["quarter_num"] = df["quarter"].str.replace("Q", "").astype(int)

# 4. Create employment rate
df["emp_rate"] = 100 - df["unemp_rate"]

# 5. Sort rows
df = df.sort_values(["state", "year", "quarter_num"])

# 6. Handle missing values (simple example)
df = df.dropna()

# 7. Save cleaned file
df.to_csv("data/clean/cleaned_data.csv", index=False)




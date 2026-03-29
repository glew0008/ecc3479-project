import pandas as pd

df = pd.read_excel(
    "data/raw/2021 census data.xlsx",
    header=None,
    dtype=str
)

# Show first 60 rows and first 20 columns
print(df.iloc[:60, :20])

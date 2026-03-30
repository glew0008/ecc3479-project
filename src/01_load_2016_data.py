import pandas as pd

df = pd.read_excel(
    "data/raw/raw_2016_data.xlsx",
    header=None,
    dtype=str
)

# Show first 60 rows and first 20 columns
print(df.iloc[:60, :20])

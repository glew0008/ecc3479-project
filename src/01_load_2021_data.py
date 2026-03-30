import pandas as pd

# Load the new 2021 file exactly as-is
df = pd.read_excel(
    "data/raw/raw_2021_data.xlsx",
    header=None,
    dtype=str
)

# Print the first 60 rows and first 20 columns
print(df.iloc[:60, :20])

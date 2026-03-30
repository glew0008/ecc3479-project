import pandas as pd

# 1. Load raw file with no header
df = pd.read_excel(
    "data/raw/raw_2016_data.xlsx",
    header=None,
    dtype=str
)

# 2. Clean column 1 (income bracket column)
df[1] = df[1].astype(str).str.strip().str.lower()

# 3. Find start and end of the income table
start_row = df[df[1].str.contains("negative income", na=False)].index[0]
end_row = df[df[1].str.contains("^total$", na=False)].index[0]

# 4. Extract only the table
df = df.loc[start_row:end_row]

# 5. Assign column names
education_levels = [
    "Postgraduate Degree Level",
    "Graduate Diploma and Graduate Certificate Level",
    "Bachelor Degree Level",
    "Advanced Diploma and Diploma Level",
    "Certificate III & IV Level",
    "Secondary Education - Years 10 and above",
    "Certificate I & II Level",
    "Secondary Education - Years 9 and below",
    "Supplementary Codes",
    "Not stated",
    "Not applicable",
    "Total"
]

df.columns = ["col0", "income_bracket"] + education_levels

# 6. Clean income bracket text
df["income_bracket"] = df["income_bracket"].str.title()

# 7. Remove rows not needed
df = df[~df["income_bracket"].isin(["Not Applicable", "Total"])]

# 8. Reshape wide → long
df_long = df.melt(
    id_vars="income_bracket",
    var_name="education",
    value_name="count"
)

df_long = df_long.dropna(subset=["count"])

# 9. Save cleaned dataset
df_long.to_csv("data/clean/2016_census_clean.csv", index=False)

print("Cleaning complete. Rows:", len(df_long))
print(df_long.head())

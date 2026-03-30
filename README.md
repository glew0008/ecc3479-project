Project Title
Education and Income in Australia: A Comparative Analysis Using 2016 and 2021 Census Data

Overview
This project investigates the relationship between educational attainment and personal income for Australian males using data from the 2016 and 2021 ABS Census.
The analysis focuses on how income distributions differ across education levels and how these patterns have changed over time.

The project follows a fully reproducible workflow, including raw data extraction, cleaning, merging, and analysis.

Research Question
How does educational attainment affect personal income for Australian males, and how did this relationship change between 2016 and 2021?

Data Sources
Data were extracted from the ABS Census TableBuilder platform.

For both 2016 and 2021, the following variables were used:

INCP – Total Personal Income (weekly)

HEAP – Highest Educational Attainment (1‑digit)

SEXP – Sex (Male)

Geography – Australia (UR)

Summation – Persons, Place of Usual Residence

Only the datasets containing both income and education variables were used:

2016 Census – Employment, Income and Education

2021 Census – Employment, Income and Education

2011 and 2006 were excluded because TableBuilder splits income and education across incompatible datasets in those years, preventing extraction of a consistent table.

Repository Structure
Code
ecc3479-project/
│
├── data/
│   ├── raw/                # Raw ABS exports (Excel/CSV)
│   └── clean/              # Cleaned, tidy datasets
│       ├── 2016_clean.csv
│       ├── 2021_clean.csv
│       └── merged_2016_2021.csv
│
├── src/
│   ├── 01_load_2016.py
│   ├── 01_load_2021.py
│   ├── 02_clean_2016.py
│   ├── 02_clean_2021.py
│   ├── 03_merge_2016_2021.py
│   └── 04_analysis.py      # (to be developed)
│
└── README.md

Cleaning Process
Each year is cleaned separately using dedicated scripts in src/.

Cleaning Steps (applied to both years)
Load the raw ABS export (CSV or Excel).

Identify the start and end of the income table.

Remove metadata rows and empty rows.

Standardise column names.

Reshape from wide to long format using pandas.melt().

Output a tidy dataset with the following schema:

Code
year
income_bracket
education
count
Output Files
data/clean/2016_clean.csv

data/clean/2021_clean.csv

Merging Process
A dedicated script (03_merge_2016_2021.py) merges the cleaned datasets into a single long-format file:

Code
data/clean/merged_2016_2021.csv
This file contains all combinations of:

year

income bracket

education level

count

and is used for all downstream analysis.

Analysis Plan
The analysis (in 04_analysis.py) will include:

Income midpoint conversion  
Convert each income bracket into a numeric midpoint for quantitative analysis.

Weighted mean income by education  
Compute weighted averages for each education level in each year.

Year‑to‑year comparison  
Examine how income distributions shifted between 2016 and 2021.

Visualisations

Income distribution by education

Change in weighted mean income

Education‑income gradients over time

Interpretation  
Discuss how the relationship between education and income has evolved.

Reproducibility Commitment
This project follows best practices for reproducible research:

Clear folder structure

Separate scripts for loading, cleaning, merging, and analysis

Meaningful commit messages

Transparent documentation of all data transformations

No manual editing of raw data

Limitations
2011 and 2006 Census data were excluded because income and education variables are not available in a single compatible dataset for those years.

Income brackets differ slightly between 2016 and 2021 (e.g., top brackets split in 2021). These differences will be handled during midpoint conversion.

Next Steps
Finalise income midpoint conversion

Complete analysis script

Produce visualisations

Write interpretation and conclusions

If you want, I can now help you write the analysis script, the midpoint conversion, or the visualisation code.
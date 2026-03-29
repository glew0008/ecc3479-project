ECC3479 Research Project — Data Pipeline & Documentation
Project Overview
This repository contains the full, reproducible workflow for my ECC3479 research project. The goal is to analyse the relationship between education level and personal income for Australian males, using publicly available ABS Census data (2016).

The project is structured around a clear, modular pipeline:

Raw data inspection

Data cleaning and reshaping

Analysis (upcoming)

Documentation and reproducibility

Repository Structure
Code
ecc3479-project/
│
├── data/
│   ├── raw/
│   │   └── 2021 census data.xlsx
│   └── clean/
│       └── 2016_census_clean.csv
│
├── src/
│   ├── 01_load_data.py
│   └── 02_clean_data.py
│
└── README.md
1. Raw Data Inspection — 01_load_data.py
This script loads the ABS Excel file exactly as it appears, without assuming any structure.
It prints the first 40–60 rows so I can visually inspect:

where metadata ends

where the income table begins

which column contains income brackets

which columns contain education-level counts

where the table ends

This step is essential because ABS TableBuilder exports often contain:

merged cells

blank rows

metadata blocks

inconsistent spacing

no true header row

Running this script ensures the cleaning pipeline is based on an accurate understanding of the raw file.

2. Data Cleaning — 02_clean_data.py
This script performs the full cleaning pipeline.

Loads the raw Excel with no header
ABS files do not contain a usable header row, so the file is read without one.

Automatically detects the income table
The script identifies the row containing “Negative income” and the row containing “Total” using robust text matching.

Extracts the income × education matrix
Only the rows and columns containing real data are kept.

Assigns correct education-level column names
These are manually defined because the raw file does not include them in a structured header.

Reshapes the dataset from wide to long
Final tidy format:

Code
income_bracket    education    count
Saves the cleaned dataset
The cleaned dataset is written to:

Code
data/clean/2016_census_clean.csv
This file is now ready for analysis.
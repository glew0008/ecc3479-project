# Education and Income in Australia

This project analyses the relationship between educational attainment and personal income for Australian males using ABS Census TableBuilder extracts from 2016 and 2021.

The repository contains the full workflow from raw Excel extracts, to cleaned long-format datasets, to a merged analysis file, to reproducible exploratory data analysis outputs and a submission notebook.

## Research Question

How does educational attainment affect personal income for Australian males, and how did this relationship change between the 2016 and 2021 Census?

## Exploratory Data Analysis

The project includes a completed EDA in `src/04_eda.py`, with outputs saved under `outputs/eda/`.

The analysis uses `data/clean/merged_2016_2021.csv` and focuses on the eight substantive education groups, excluding administrative categories such as `Total`, `Not stated`, `Not applicable`, and `Supplementary Codes`. To improve comparability across Census years, the split 2021 top-income categories are harmonised into a single top bracket, and income brackets are converted to approximate numeric midpoints for weighted summary analysis.

### EDA highlights

- The merged dataset contains 396 rows, with 248 rows in the analytic sample.
- The total weighted population count in the analytic sample is 16,788,600.
- The overall income distribution shifts upward between 2016 and 2021.
- Postgraduate Degree Level has the highest estimated weekly income in both years.
- Bachelor Degree Level shows the largest increase in weighted mean weekly income between 2016 and 2021.
- The education-income gradient is very strong in both years, with weighted correlations close to 1.

### Main EDA outputs

- Narrative report: `outputs/eda/eda_report.md`
- Submission notebook: `outputs/eda/eda_submission.ipynb`
- Tables: `outputs/eda/tables/`
- Figures: `outputs/eda/figures/`

For the full written interpretation, see [eda_report.md](/c:/Users/gdlew/OneDrive/MONASH/Yr%203%20Sem%201/ECC3479%20Data%20and%20Evidence%20in%20economics/ecc3479-project/outputs/eda/eda_report.md).

## Data Source

The data were extracted from ABS Census TableBuilder.

Variables used:

- `INCP` - Total Personal Income (weekly)
- `HEAP` - Highest Educational Attainment (1-digit)
- `SEXP` - Sex (Male)
- Geography - Australia (UR)
- Summation - Persons, Place of Usual Residence

The project uses the 2016 and 2021 Census employment, income, and education tables. Earlier Census years were excluded because income and education were not available in one directly comparable extract.

## Repository Structure

```text
ecc3479-project/
├── data/
│   ├── raw/
│   │   ├── raw_2016_data.xlsx
│   │   ├── raw_2021_data.xlsx
│   │   └── READ.md
│   └── clean/
│       ├── 2016_census_clean.csv
│       ├── 2021_census_clean.csv
│       ├── merged_2016_2021.csv
│       └── codebook.md
├── outputs/
│   └── eda/
│       ├── eda_report.md
│       ├── eda_submission.ipynb
│       ├── figures/
│       └── tables/
├── src/
│   ├── 01_load_2016_data.py
│   ├── 01_load_2021_data.py
│   ├── 02_clean_2016_data.py
│   ├── 02_clean_2021_data.py
│   ├── 03_merge_data_sets.py
│   └── 04_eda.py
└── README.md
```

## Workflow

### 1. Raw data inspection

- `src/01_load_2016_data.py`
- `src/01_load_2021_data.py`

These scripts load the raw ABS Excel files and print the first part of each sheet so the structure can be inspected before cleaning.

### 2. Cleaning each Census extract

- `src/02_clean_2016_data.py`
- `src/02_clean_2021_data.py`

Each cleaning script:

- loads the raw Excel file with no header
- finds the income table inside the ABS export
- assigns education column names
- removes unwanted summary rows
- reshapes the table from wide to long format
- saves the cleaned output to `data/clean/`

Output files:

- `data/clean/2016_census_clean.csv`
- `data/clean/2021_census_clean.csv`

### 3. Merging both years

- `src/03_merge_data_sets.py`

This script appends the cleaned 2016 and 2021 files, adds a `year` variable where needed, standardises column order, and saves:

- `data/clean/merged_2016_2021.csv`

### 4. Exploratory data analysis

- `src/04_eda.py`

This script:

- loads the merged dataset
- harmonises the top income bracket so 2016 and 2021 are comparable
- converts income brackets to numeric midpoints for weighted summaries
- excludes non-analytic education categories from the main comparisons
- produces summary tables and figures
- writes the narrative report used in the notebook submission

Main output locations:

- `outputs/eda/tables/`
- `outputs/eda/figures/`
- `outputs/eda/eda_report.md`

### 5. Notebook submission

- `outputs/eda/eda_submission.ipynb`

This notebook is the submission-ready deliverable. It loads the generated report, tables, and figures from `outputs/eda/`.

## Clean Dataset Structure

The merged dataset in `data/clean/merged_2016_2021.csv` is long format, where each row represents one `year x income_bracket x education` combination.

Variables:

- `year` - Census year, either `2016` or `2021`
- `income_bracket` - ABS weekly personal income bracket
- `education` - highest educational attainment category
- `count` - number of Australian males in that cell

More detail is documented in [codebook.md](/c:/Users/gdlew/OneDrive/MONASH/Yr%203%20Sem%201/ECC3479%20Data%20and%20Evidence%20in%20economics/ecc3479-project/data/clean/codebook.md).

## Detailed EDA Outputs

### Tables

The current EDA script produces:

- `outputs/eda/tables/data_quality_summary.csv`
- `outputs/eda/tables/variable_overview.csv`
- `outputs/eda/tables/cleaning_summary.csv`
- `outputs/eda/tables/weighted_income_describe_by_year.csv`
- `outputs/eda/tables/education_income_summary.csv`
- `outputs/eda/tables/correlation_summary.csv`
- `outputs/eda/tables/education_year_over_year_change.csv`
- `outputs/eda/tables/income_distribution_by_education.csv`
- `outputs/eda/tables/top_income_bracket_summary.csv`

### Figures

The current EDA script produces:

- `outputs/eda/figures/population_by_education_year.png`
- `outputs/eda/figures/weighted_income_boxplot_by_year.png`
- `outputs/eda/figures/income_ecdf_by_year.png`
- `outputs/eda/figures/weighted_mean_income_by_education.png`
- `outputs/eda/figures/first_order_effect_education_income.png`
- `outputs/eda/figures/income_distribution_heatmap_2016.png`
- `outputs/eda/figures/income_distribution_heatmap_2021.png`
- `outputs/eda/figures/income_distribution_change_heatmap.png`
- `outputs/eda/figures/weighted_mean_income_change.png`
- `outputs/eda/figures/overall_income_distribution_by_year.png`
- `outputs/eda/figures/top_income_share_by_education.png`

### Report

The main written EDA output is:

- `outputs/eda/eda_report.md`

## Key EDA Findings

The current exploratory analysis shows:

- a strong positive education-income gradient in both 2016 and 2021
- higher estimated income levels for higher-attainment education groups
- an upward shift in the overall income distribution from 2016 to 2021
- particularly strong top-income representation among postgraduate degree holders
- very high weighted correlations between education rank and weighted mean income

For the full narrative and interpretation, see [eda_report.md](/c:/Users/gdlew/OneDrive/MONASH/Yr%203%20Sem%201/ECC3479%20Data%20and%20Evidence%20in%20economics/ecc3479-project/outputs/eda/eda_report.md).

## How To Run

### Environment setup

Create and activate a virtual environment, then install the required packages:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the notebook is opened in Jupyter, select the `.venv` kernel before running all cells.

Run the scripts from the project root.

### Cleaning

```powershell
.venv\Scripts\python.exe src/02_clean_2016_data.py
.venv\Scripts\python.exe src/02_clean_2021_data.py
```

### Merge

```powershell
.venv\Scripts\python.exe src/03_merge_data_sets.py
```

### EDA

```powershell
.venv\Scripts\python.exe src/04_eda.py
```

### Notebook

After generating the EDA outputs, open `outputs/eda/eda_submission.ipynb`, restart the kernel if needed, and run the notebook from top to bottom.

## Reproducibility Notes

This project is organised to support a reproducible workflow:

- raw source files are kept in `data/raw/`
- cleaned data are generated by scripts in `src/`
- merged and analysis-ready data are stored in `data/clean/`
- EDA tables, figures, and report outputs are written to `outputs/eda/`
- the submission notebook reads generated files rather than relying on manual copy-paste

## Submission Package

To let another person replicate the notebook, submit the full project folder as a zip archive with:

- `README.md`
- `requirements.txt`
- `src/`
- `data/raw/`
- `data/clean/`
- `outputs/eda/`

Do not include `.venv/` or `.git/`.

After unzipping, the replication steps are:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.venv\Scripts\python.exe src/02_clean_2016_data.py
.venv\Scripts\python.exe src/02_clean_2021_data.py
.venv\Scripts\python.exe src/03_merge_data_sets.py
.venv\Scripts\python.exe src/04_eda.py
```

Then open `outputs/eda/eda_submission.ipynb` and run all cells from top to bottom.

## Limitations

- The analysis is restricted to Australian males because that is how the TableBuilder extract was defined.
- Income is observed in brackets, so midpoint conversion is an approximation rather than an exact individual income measure.
- The top income bracket differs across years and must be harmonised for comparability.
- Administrative education labels such as `Total`, `Not stated`, `Not applicable`, and `Supplementary Codes` are not used in the main substantive comparisons.

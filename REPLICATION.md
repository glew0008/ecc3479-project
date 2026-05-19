# Replication Guide

This repository contains the complete replication package for the analysis reported in `docs/project_report_v2.pdf`.

## Files and folders

- `data/raw/`
  - `raw_2016_data.xlsx`
  - `raw_2021_data.xlsx`
  - `READ.md`
  - Raw ABS TableBuilder extracts used to produce the cleaned analytic dataset.
- `data/clean/`
  - `2016_census_clean.csv`
  - `2021_census_clean.csv`
  - `merged_2016_2021.csv`
  - `codebook.md`
  - Cleaned datasets used for analysis.
- `src/`
  - `01_load_2016_data.py`
  - `01_load_2021_data.py`
  - `02_clean_2016_data.py`
  - `02_clean_2021_data.py`
  - `03_merge_data_sets.py`
  - `04_eda.py`
  - `robustness_analysis.py`
  - Analysis and data-preparation scripts.
- `outputs/eda/`
  - `eda_report.md`
  - `eda_submission.ipynb`
  - `tables/`
  - `figures/`
- `outputs/analysis/`
  - `robustness_table.csv`
- `docs/`
  - `report.md`
  - `project_report_v2.pdf`
- `scripts/`
  - `generate_report_pdf.py`

## Reproducing the cleaned data

From the project root, run:

```powershell
.\.venv\Scripts\python.exe src\01_load_2016_data.py
.\.venv\Scripts\python.exe src\01_load_2021_data.py
.\.venv\Scripts\python.exe src\02_clean_2016_data.py
.\.venv\Scripts\python.exe src\02_clean_2021_data.py
.\.venv\Scripts\python.exe src\03_merge_data_sets.py
```

This produces the cleaned files in `data/clean/`.

## Reproducing the EDA tables and figures

Run:

```powershell
.\.venv\Scripts\python.exe src\04_eda.py
```

This writes the main tables to `outputs/eda/tables/` and figures to `outputs/eda/figures/`.

## Reproducing the robustness analysis

Run:

```powershell
.\.venv\Scripts\python.exe src\robustness_analysis.py
```

This writes `outputs/analysis/robustness_table.csv`.

## Reproducing the PDF report

Run:

```powershell
.\.venv\Scripts\python.exe scripts\generate_report_pdf.py
```

This generates `docs/project_report_v2.pdf` from `docs/report.md` and the figures in `outputs/eda/figures/`.

## Mapping tables and figures in the report

- Table of weighted mean income by year: produced by `src/04_eda.py` and saved to `outputs/eda/tables/weighted_income_describe_by_year.csv`.
- Figure 1: `outputs/eda/figures/weighted_mean_income_by_education.png`.
- Figure 2: `outputs/eda/figures/top_income_share_by_education.png`.
- Main regression and robustness results: produced by `src/robustness_analysis.py` and saved to `outputs/analysis/robustness_table.csv`.

## Notes

All scripts use the virtual environment in `.venv/`. If the virtual environment is not active, invoke the explicit interpreter above. The repository is self-contained: the raw ABS extracts and the code needed to reproduce the clean data, analysis outputs, and PDF report are all included.

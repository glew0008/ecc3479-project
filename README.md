# ecc3479-project
This project investigates the effect of obtaining a bachelor’s degree on annual income for males in Australia between 2005 and 2025 compared to males without a bachelor’s degree.

Data sources -> ABS, Hilda survey, Census

Group Members -> George Lewis

We commit to maintaining full research transparency by documenting every major decision, using clear and consistent commit messages, and recording any use of AI tools along with how outputs were verified.

## 📁 Repository Structure
project/
│
├── data/
│   ├── raw/        # Raw HILDA files (not uploaded to GitHub)
│   └── clean/      # Cleaned, analysis-ready dataset + codebook
│
├── code/
│   ├── 01_load_data.py
│   ├── 02_clean_data.py
│   └── 03_analysis.py
│
├── output/         # Figures, tables, regression results
│
└── README.md

---

## 🚀 How to Run This Project From Scratch

### **1. Obtain the raw data**
Due to licensing restrictions, HILDA microdata cannot be uploaded to GitHub.  
To reproduce this project:

1. Apply for HILDA access through the Australian Data Archive (ADA).  
2. Download the STATA `.dta` files.  
3. Place them inside:

data/raw/

### **2. Install required software**
This project uses:

- Python 3.x  
- pandas  
- numpy  
- statsmodels  
- matplotlib / seaborn  

You can install everything with:

pip install -r requirements.txt


(You can create this file later.)

---

## 🧪 Script Execution Order

Run the scripts in the following order:

1. `01_load_data.py`  
   - Loads raw HILDA files  
   - Selects relevant variables  
   - Saves intermediate dataset  

2. `02_clean_data.py`  
   - Filters males aged 15–74  
   - Creates bachelor indicator  
   - Creates income variable  
   - Saves cleaned dataset to `data/clean/`  

3. `03_analysis.py`  
   - Computes descriptive statistics  
   - Runs regression  
   - Exports tables/figures to `output/`  

---

## 📘 Data Codebook

A full codebook describing all variables in the cleaned dataset is located in:

data/clean/codebook.md

This includes:

- Variable names  
- Definitions  
- Units  
- Transformations  
- Source files  

---

## 🔍 Research Transparency

This repository follows best practices for reproducible research:

- Frequent, meaningful commit messages  
- Clear documentation of all decisions  
- No raw data uploaded (due to licensing)  
- All analysis steps fully scripted  
- AI usage documented and verified  





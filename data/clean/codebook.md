
The dataset contains one row for every combination of:

- Census year  
- Weekly personal income bracket  
- Highest educational attainment  
- Count of males in that category  

It is produced by merging the cleaned 2016 and 2021 Census tables extracted from ABS TableBuilder.

---

## Dataset Structure

| Variable         | Type        | Description |
|------------------|-------------|-------------|
| `year`           | Integer     | Census year (2016 or 2021) |
| `income_bracket` | Categorical | Weekly personal income bracket (string label from ABS) |
| `education`      | Categorical | Highest educational attainment (string label from ABS) |
| `count`          | Integer     | Number of males in that income × education × year cell |

---

# Variable Definitions

## 1. year
- **Type:** Integer  
- **Values:** `2016`, `2021`  
- **Source:** Added during cleaning  
- **Meaning:** Identifies which Census year the row belongs to  
- **Notes:**  
  - Derived from separate raw tables  
  - Ensures both years can be stacked in long format  

---

## 2. income_bracket
- **Type:** Categorical (string)  
- **Source:** ABS Census TableBuilder — INCP (Total Personal Income, weekly)  
- **Meaning:** Weekly personal income bracket  
- **Examples of values:**  
  - `Negative Income`  
  - `Nil Income`  
  - `$1-$149 ($1-$7,799)`  
  - `$150-$299 ($7,800-$15,599)`  
  - `$300-$399 ($15,600-$20,799)`  
  - `$400-$499 ($20,800-$25,999)`  
  - `$500-$649 ($26,000-$33,799)`  
  - `$650-$799 ($33,800-$41,599)`  
  - `$800-$999 ($41,600-$51,999)`  
  - `$1,000-$1,249 ($52,000-$64,999)`  
  - `$1,250-$1,499 ($65,000-$77,999)`  
  - `$1,500-$1,749 ($78,000-$90,999)`  
  - `$1,750-$1,999 ($91,000-$103,999)`  
  - `$2,000-$2,999 ($104,000-$155,999)`  
  - **2016 top bracket:** `$3,000 Or More ($156,000 Or More)`  
  - **2021 top brackets:**  
    - `$3,000-$3,499 ($156,000-$181,999)`  
    - `$3,500 Or More ($182,000 Or More)`  

- **Notes:**  
  - 2021 splits the top bracket into two; 2016 uses one combined bracket  
  - These will be converted to numeric midpoints during analysis  
  - Brackets are mutually exclusive and exhaustive  

---

## 3. education
- **Type:** Categorical (string)  
- **Source:** ABS Census TableBuilder — HEAP (Highest Educational Attainment)  
- **Meaning:** Highest level of education completed  
- **Examples of values:**  
  - Postgraduate Degree Level  
  - Graduate Diploma and Graduate Certificate Level  
  - Bachelor Degree Level  
  - Advanced Diploma and Diploma Level  
  - Certificate III & IV Level  
  - Certificate I & II Level  
  - Secondary Education – Years 10 and above  
  - Secondary Education – Years 9 and below  
  - Supplementary Codes  
  - Not stated  
  - Not applicable  
  - Total  

- **Notes:**  
  - “Total” rows represent the sum across all education categories  
  - “Not applicable” rows contain zeros (e.g., children, non‑respondents)  
  - “Not stated” is a valid Census category  
  - “Supplementary Codes” includes special ABS classifications  

---

## 4. count
- **Type:** Integer  
- **Source:** ABS TableBuilder — Persons, Place of Usual Residence  
- **Meaning:** Number of males in that income × education × year cell  
- **Notes:**  
  - These are weighted population counts  
  - Used for computing weighted mean income  
  - No missing values  

---

# Data Provenance

- Raw data extracted from ABS Census TableBuilder (2016 and 2021)  
- Filters applied:  
  - **Sex:** Male  
  - **Geography:** Australia (UR)  
  - **Summation:** Persons  
- Cleaned using scripts in `src/`  
- Merged using `03_merge_data_sets.py`  

---

# Transformations Applied

1. Removed metadata rows from raw ABS exports  
2. Standardised column names  
3. Reshaped wide tables into long format  
4. Added `year` variable  
5. Ensured consistent variable order  
6. Combined 2016 and 2021 into a single dataset  

No manual edits were made to the data.

---

# File Output

The final analysis‑ready dataset is saved as:
data/clean/merged_2016_2021.csv



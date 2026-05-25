# Education and Income in Australia: A Reproducible Analysis

## Introduction

This report studies whether higher educational attainment is associated with higher weekly personal income for Australian males, and whether that relationship changed between the 2016 and 2021 Census. The question matters because the education-income gradient is a key driver of inequality and workforce planning. Policy discussions often assume that higher qualifications reliably translate into higher earnings, but the strength of that association can vary with labour market conditions, credential supply, and the relative returns to different qualification levels.

Using ABS Census TableBuilder extracts, the analysis documents the population-level relationship across eight substantive education groups, compares income outcomes between 2016 and 2021, and tests whether the headline association is robust to alternative definitions of the outcome, the sample, and the estimation method. The analysis is explicitly descriptive: it reports the shape and magnitude of the education-income gradient in these grouped census data while clearly recognising that the grouped nature of the data does not permit a causal interpretation.

The main finding is strong and internally consistent. In the analytic sample, each additional step in the ordered education hierarchy is associated with roughly **$196 more per week** in weighted mean income, controlling for year. This pattern is visible in both censuses, and it holds across a battery of alternative specifications.

## Data

### Sources and preparation

The dataset is built from two ABS Census TableBuilder extracts for Australian males:

- 2016 Census: personal weekly income by highest educational attainment.
- 2021 Census: personal weekly income by highest educational attainment.

The raw files are stored in `data/raw/raw_2016_data.xlsx` and `data/raw/raw_2021_data.xlsx`. The cleaning pipeline is implemented in `src/01_load_2016_data.py`, `src/01_load_2021_data.py`, `src/02_clean_2016_data.py`, `src/02_clean_2021_data.py`, and `src/03_merge_data_sets.py`.

### Sample construction

The analytic sample excludes non-substantive and administrative categories that do not represent a meaningful education group:

- `Total`
- `Not stated`
- `Not applicable`
- `Supplementary Codes`

This removes rows that represent summary totals, missing responses, or classification codes rather than actual attainment groups. The remaining analytic sample therefore focuses on the eight educational attainment categories that are comparable across both censuses.

The 2021 extract includes two separate top-income categories. These were harmonised to a single open-ended top bracket, `$3,000 Or More ($156,000 Or More)`, to allow direct comparison with 2016. Income brackets are converted to weekly midpoint values to support weighted mean calculations and regression outcomes.

### Variables and analytic dataset

The cleaned merged dataset is saved to `data/clean/merged_2016_2021.csv` and documented in `data/clean/codebook.md`. The analysis focuses on an analytic sample of 248 rows after excluding non-substantive education labels and unstated income values.

Key variables and their roles in the analysis:

- `year` (integer): Census year, either `2016` or `2021`. This is the main time indicator used to separate the two Census waves.
- `education` (categorical): highest educational attainment category. Only eight substantive groups are used for the main analysis; administrative categories such as `Total`, `Not stated`, `Not applicable`, and `Supplementary Codes` are excluded.
- `income_bracket` (categorical): ABS weekly personal income bracket. The raw brackets come from Census TableBuilder.
- `count` (integer): number of Australian males in each `year × income_bracket × education` cell. These are the population weights used in all weighted summaries and regressions.
- `education_rank` (integer): ordinal score from 1 to 8 assigned to the analytic education groups. It is the main independent variable in the regression specification.
- `income_midpoint` (numeric): estimated weekly income midpoint for each income bracket.
- `weighted_income` (numeric): the product of `income_midpoint` and `count`, used to compute weighted mean income.

The dependent variable in the main regression is the weighted mean weekly income for each education-year cell. The main independent variable is the education rank, which preserves the natural ordering of attainment categories without imposing a precise cardinal distance between them.

### Summary statistics

After cleaning and harmonising, the analytic dataset contains 248 substantive rows and represents a weighted population of approximately **16.8 million Australian males**.

The two census years differ noticeably in their overall income distribution:

- 2016 weighted mean weekly income: **$1,053.56**.
- 2021 weighted mean weekly income: **$1,208.03**.
- 2016 weighted median weekly income: **$899.50**.
- 2021 weighted median weekly income: **$1,124.50**.

The interquartile range shifts upward from **$349.50-$1,624.50** in 2016 to **$449.50-$1,624.50** in 2021, indicating a general rightward shift in the income distribution.

The education groups show a strong rank-order relationship with income. In both years, the highest group is **Postgraduate Degree Level** and the lowest is **Secondary Education - Years 9 and below**.

## Empirical strategy

### Model and variables

The main empirical model is a weighted linear regression estimated on education-year cells:

`MeanIncome_{ey} = alpha + beta * EducationRank_e + gamma * Year2021_y + epsilon_{ey}`

where:

- `MeanIncome_{ey}` is the weighted mean weekly income for education group `e` in year `y`.
- `EducationRank_e` is an ordinal rank from 1 to 8 assigned to the eight substantive education groups.
- `Year2021_y` is a year indicator equal to 1 for 2021 and 0 for 2016.
- weights are the population counts (`count`) for each education-income cell.

The dependent variable is constructed from group-level income brackets; the analysis approximates each bracket by its midpoint and computes a weighted mean income for each education-year cell. The main independent variable is the education rank, which contains the ordered information from low to high attainment. The year indicator captures the overall shift in incomes between Census waves.

### Identification and assumptions

This analysis is descriptive rather than causal. A causal interpretation would require the assumption that, after controlling for year, education rank is independent of all other factors that affect income. That assumption is not credible here because the grouped Census data do not control for important individual-level confounders such as age, labour-force status, occupation, hours worked, industry, or geographic location.

The core identifying assumption for the headline association is therefore very weak. The result should be read as a population-level association between higher education categories and higher average incomes in the Census aggregates, not as a causal return to education.

### Measurement choices

- `education_rank` is ordinal and reflects the ordered level of education categories; it should not be interpreted as a precise number of years or quality units.
- Income brackets are converted to weekly midpoints. The top open-ended income bracket is harmonised across years to allow direct comparison.
- A subset of tables excludes `Not Stated` income rows so the mean income calculations reflect actual reported income brackets.

### Weighting and sample

Weighting by cell count is essential because each row represents a different number of people. Without weights, small education-income cells would count the same as very large ones, which would distort the population-level relationship.

The analytic sample excludes rows with administrative education labels and unstated income, leaving 248 substantive cells that represent about 16.8 million Australian males.

## Results

### Main regression

The main weighted regression estimate is:

- `EducationRank` coefficient: **$195.88** per rank step.
- standard error: **$7.38**.
- p-value: **< 0.001**.
- `Year2021` coefficient: **$120.75** additional weekly income.

The sample for this regression represents about **16.8 million observations** in population counts and uses the eight substantive education groups with reported income.

In plain language:

- A one-step increase in education rank is associated with about **$196 more per week** in the group’s mean weekly income.
- The difference between the lowest and highest analytic education categories is roughly **seven rank steps × $196 = $1,372 per week**, which is equivalent to about **$71,300 per year**.
- Controlling for Census year, the 2021 mean income is estimated to be about **$121 per week higher** than 2016.

The model does not include additional individual-level controls because the aggregated Census data do not provide age, occupation, hours or regional detail at the same education-income cell level.

### Education group patterns

The education-income gradient is strong in the descriptive data:

- In 2021, **Postgraduate Degree Level** has the highest estimated mean weekly income at **$1,892.87**.
- In 2021, **Graduate Diploma and Graduate Certificate Level** has the second-highest mean weekly income at **$1,843.93**.
- In 2021, **Bachelor Degree Level** has a mean weekly income of **$1,704.55**.
- In 2021, **Secondary Education - Years 9 and below** has the lowest mean weekly income at **$506.76**.
- The lowest attainment group in 2021 has **36.41%** of its weighted population in low-income brackets, while the highest attainment group has **44.31%** in the top two income brackets.

These patterns show that education is associated not only with higher average income, but also with a systematically different position in the income distribution.

### Interpretation

The coefficient should be interpreted as a descriptive gradient rather than a causal return. It summarizes how the mean weekly income of education-year cells changes as the education category increases by one rank step, given the estimation sample and the bracket-to-midpoint income approximation.

### Visualization

![Figure 1. Weighted mean weekly income by education and census year.](outputs/eda/figures/weighted_mean_income_by_education.png)

Figure 1 shows a monotonic increase in mean income across education ranks in both years, with all groups shifting upward from 2016 to 2021.

### Distributional evidence

The distributional charts produced in the EDA reinforce the primary finding. Higher attainment groups are concentrated in upper income brackets, while lower attainment groups are concentrated in lower brackets. This suggests the education-income relationship is present across the income distribution rather than being driven solely by a few outliers.

## Robustness

The headline association is robust across a battery of specification checks. These results are summarised in `outputs/analysis/robustness_table.csv`.

### Specification checks

- `Main`: weighted least squares with the year control yields a coefficient of **$195.88** for `education_rank`.
- `No controls`: dropping the year indicator produces a similar coefficient of **$197.17**, showing the gradient is not driven solely by the year shift.
- `Drop top bracket`: excluding the top open-ended income bracket lowers the coefficient to **$145.74**, which shows the highest incomes do have an important influence on the group means.
- `IHS outcome`: using inverse hyperbolic sine of income preserves the positive association in a log-like transformation.
- `Log outcome`: applying a natural log to positive incomes also maintains the association, although it removes zero and negative values from the sample.
- `2021 only`: the 2021 sample alone produces a coefficient of **$202.64**.
- `2016 only`: the 2016 sample alone produces a coefficient of **$187.77**.
- `HC0 SE`: heteroskedasticity-robust standard errors leave the point estimate unchanged at **$195.88**, with a robust standard error of **$8.72**.
- `Unweighted OLS`: an unweighted regression yields **$205.16**, showing that the weighted finding is not an artifact of the chosen sample weights.
- `Exclude negative income`: dropping negative-income observations changes the coefficient only slightly to **$195.25**.

### What this robustness tells us

The main descriptive association is stable across sensible alternative model choices and sample definitions. The largest sensitivity comes from excluding the open-ended top-income bracket, which is expected because high incomes are concentrated in the top education groups and can disproportionately affect group means.

### Visualization

![Figure 2. Top income share by education group in the analytic sample.](outputs/eda/figures/top_income_share_by_education.png)

Figure 2 shows that higher education groups hold larger shares of top-income brackets, while lower education groups hold larger shares of low-income brackets.

## Discussion, limitations, and conclusion

### What the data support

- There is a strong descriptive association between higher educational attainment and higher weekly income for Australian males in the Census aggregates.
- The gradient exists in both 2016 and 2021 and remains when controlling for the overall year-to-year income shift.
- Higher education groups are consistently more represented in upper income brackets, while lower education groups are concentrated in lower brackets.

### What this analysis cannot establish

- It cannot establish a causal return to education. The data are grouped and do not support individual-level identification.
- The analysis cannot adjust for age, occupation, hours worked, industry, region, or labour force status within the same education-income cells.
- Income is measured in brackets, so the numeric outcome is an approximation from bracket midpoints rather than a precise individual income value.
- The education rank is ordinal, not cardinal. A one-step change in rank means moving to the next education category, not gaining a fixed number of schooling years.

### The most important remaining threat

The largest interpretive threat is omitted-variable bias from compositional differences across education groups. For example:

- higher education groups tend to be older and more likely to work full-time,
- they may be concentrated in higher-paying industries and occupations,
- and they are likely to differ in geographic location and labour market attachment.

These omitted differences can explain part of the income gap even if education itself is not the only causal driver.

### How to improve the design

The most credible next step is to use individual-level microdata with controls for age, occupation, industry, hours worked, region, and labour-force status. Better yet, a quasi-experimental design using exogenous variation in education attainment — such as a schooling reform or instrumented changes in qualifications — would be required for causal inference.

Longitudinal or panel data would also help distinguish whether the observed 2016–2021 differences reflect changing cohort composition or true shifts in the returns to education.

## References

Australian Bureau of Statistics. Census TableBuilder. 2016 and 2021.

Angrist, Joshua D., and Jörn-Steffen Pischke. *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press, 2009.

Card, David. "The Causal Effect of Education on Earnings." In *Handbook of Labor Economics*, vol. 3, 1999.

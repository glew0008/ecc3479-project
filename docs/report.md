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

The cleaned merged dataset is saved to `data/clean/merged_2016_2021.csv` and documented in `data/clean/codebook.md`. Key variables include:

- `year`: census year (2016 or 2021).
- `education`: highest educational attainment category.
- `income_bracket`: ABS weekly personal income bracket.
- `count`: number of persons in the cell.
- `education_rank`: ordinal score from 1 (lowest analytic attainment) to 8 (highest attainment).
- `income_midpoint`: estimated weekly income midpoint for the bracket.
- `weighted_income`: midpoint times cell count.

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

### Specification

The main empirical model is a weighted linear specification estimated on education-year cells:

`MeanIncome_{ey} = alpha + beta * EducationRank_e + gamma * Year2021_y + epsilon_{ey}`

where:

- `MeanIncome_{ey}` is the weighted mean weekly income for education group `e` in year `y`.
- `EducationRank_e` is an ordinal rank from 1 to 8.
- `Year2021_y` is an indicator equal to 1 for 2021 and 0 for 2016.
- weights are the population counts for each cell.

The key coefficient, `beta`, measures the average increase in weighted mean income associated with one additional step in the education hierarchy.

### Descriptive ambition

This analysis is deliberately descriptive rather than causal. The census extract is grouped at the education-income-cell level and lacks individual-level controls for age, hours worked, occupation, industry, or region. Therefore, the results describe the education-income gradient in the population aggregates, but they do not identify the causal return to education.

A causal interpretation would require an assumption that, after controlling for year, education rank is exogenous to income. That assumption is unrealistic in this dataset because education groups differ systematically in many unobserved dimensions.

### Weighting and measurement

Weighting by cell count is essential because each row represents a differing number of persons. Without weights, rare education-income cells would be treated equally to large cells, distorting the population-level relationship.

Income is measured in brackets, so the analysis uses bracket midpoints as an approximation. This is a common approach for grouped income data, but it introduces measurement error, especially for the top open-ended bracket.

## Results

### Main regression

The main weighted regression estimate is:

- `EducationRank` coefficient: **$195.88** per rank step.
- standard error: **$7.38**.
- p-value: **< 0.001**.
- `Year2021` coefficient: **$120.75** additional weekly income.

In plain language:

- A one-step increase in education rank is associated with about **$196 more per week** in the mean income of that education group.
- The gap between the lowest and highest analytic education categories is roughly **7 × $196 = $1,372 per week**, equivalent to about **$71,344 per year**.
- The education gradient remains large even after controlling for the overall increase in income from 2016 to 2021.

### Education group patterns

The education-income gradient is strong in the descriptive data:

- In 2021, **Postgraduate Degree Level** has the highest estimated mean weekly income at **$1,892.87**.
- In 2021, **Graduate Diploma and Graduate Certificate Level** has the second-highest mean income at **$1,843.93**.
- In 2021, **Bachelor Degree Level** has a mean of **$1,704.55**.
- In 2021, **Secondary Education - Years 9 and below** has the lowest mean income at **$506.76**.
- The low-attainment group in 2021 has **36.41%** of its weighted population in low-income brackets, while the highest-attainment group has **44.31%** in the top two income brackets.

These patterns show that education is associated not only with higher average income, but also with a systematically different position in the income distribution.

### Visualization

![Figure 1. Weighted mean weekly income by education and census year.](outputs/eda/figures/weighted_mean_income_by_education.png)

Figure 1 shows a monotonic increase in mean income across education ranks in both years, with all groups shifting upward from 2016 to 2021.

### Distributional evidence

The distributional charts produced in the EDA reinforce the primary finding. Higher attainment groups are concentrated in upper income brackets, while lower attainment groups are concentrated in lower brackets. This suggests the education-income relationship is present across the income distribution rather than being driven solely by a few outliers.

## Robustness

The headline association survives multiple alternative checks.

### Specification checks

- `No controls`: omitting the year indicator still produces a large, significant coefficient.
- `Drop top bracket`: excluding the open-ended `$3,000 Or More` category lowers the coefficient to **$145.74**, indicating the top bracket has a meaningful influence.
- `IHS outcome`: using inverse hyperbolic sine of income preserves the positive association.
- `Log outcome`: using log income (excluding zero and negative values) also preserves the association.
- `HC0 SE`: heteroskedasticity-robust standard errors leave the point estimate unchanged at **$195.88**, with a robust standard error of **$8.72**.
- `Unweighted OLS`: the unweighted model yields **$205.16**, suggesting the weighted result is not solely due to weighting.
- `2016 only`: the 2016 sample yields **$187.77**.
- `2021 only`: the 2021 sample yields **$202.64**.
- `Exclude negative income`: dropping negative-income observations does not materially change the main association.

### Interpretation

The consistency of the estimate across these checks strengthens the descriptive conclusion. The largest change occurs when the top open-ended bracket is excluded, which is reasonable because that category contains the highest incomes and therefore has an outsized effect on group means.

### Visualization

![Figure 2. Top income share by education group in the analytic sample.](outputs/eda/figures/top_income_share_by_education.png)

Figure 2 shows that higher education groups hold larger shares of top-income brackets, while lower education groups hold larger shares of low-income brackets.

## Discussion, limitations, and conclusion

### What the data support

- There is a strong descriptive association between higher educational attainment and higher weekly income in the census aggregates.
- The gradient is visible in both 2016 and 2021 and remains after controlling for year.
- Higher education groups are consistently over-represented in the upper income brackets.

### What we cannot conclude

- The results do not establish a causal return to education.
- The grouped nature of the data prevents controlling for important individual-level variables such as age, hours worked, occupation, industry, and region.
- The income measure is an approximation from bracket midpoints, especially imprecise for the top open-ended bracket.
- Education rank is ordinal but not cardinal, so the coefficient should not be interpreted as a constant dollar return per qualification.

### Key interpretive threat

The most important threat is omitted-variable bias in the aggregates. Different education groups likely differ systematically in age structure, labour force participation, occupation, and location, which can generate an income gap even if the direct causal effect of education is smaller.

### Further data and design

A more credible analysis would use individual-level microdata with controls for age, occupation, industry, hours worked, and geography. Even stronger would be a quasi-experimental design using exogenous variation in education attainment, such as policy changes or schooling reforms. Longitudinal data that follow individuals over time would also help separate trends in cohort composition from true returns to education.

## References

Australian Bureau of Statistics. Census TableBuilder. 2016 and 2021.

Angrist, Joshua D., and Jörn-Steffen Pischke. *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press, 2009.

Card, David. "The Causal Effect of Education on Earnings." In *Handbook of Labor Economics*, vol. 3, 1999.

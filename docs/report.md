# Education and Income in Australia: A Reproducible Analysis

## Introduction

This project studies how educational attainment relates to weekly personal income for Australian males, and whether that relationship changed between the 2016 and 2021 Census. The question matters because education is frequently cited as a key pathway to higher earnings, but the strength and persistence of that association can vary with changing labour market conditions. Using ABS Census TableBuilder extracts, the analysis compares weighted mean income across eight substantive education groups and documents the robustness of the education-income gradient.

The main finding is clear and consistent: in the aggregate census data, each additional step in the ordered education hierarchy is associated with roughly an extra $196 in weekly income, holding the census year constant. The income gradient is strong in both years, with higher education groups concentrated in the top income brackets and lower education groups concentrated in the lower brackets. The association survives a battery of robustness checks, although the exact magnitude is somewhat attenuated if the open-ended top income bracket is excluded.

## Data

The analysis uses two ABS Census TableBuilder extracts for Australian males: one from 2016 and one from 2021. Each extract includes counts of males by highest educational attainment and weekly personal income bracket for persons in their place of usual residence.

Key data features and sample construction:

- Data sources: ABS Census TableBuilder extracts for 2016 and 2021.
- Population: Australian males only, by design of the extract.
- Analytic variables: income bracket, highest educational attainment, census year, and cell count.
- Education sample: eight substantive attainment categories.
- Exclusions: administrative labels such as `Total`, `Not stated`, `Not applicable`, and `Supplementary Codes` are excluded from the main analytic comparison.
- Income handling: the 2021 split top-income categories are harmonised into a single open-ended top bracket and income brackets are converted to weekly midpoints for weighted summaries.

After cleaning and harmonising, the merged analytic dataset contains 248 substantive rows and represents a weighted population of approximately 16.8 million male Australians.

### Summary statistics

Weighted income rises between the two census years.

- 2016 weighted mean weekly income: $1,053.56.
- 2021 weighted mean weekly income: $1,208.03.
- 2016 weighted median weekly income: $899.50.
- 2021 weighted median weekly income: $1,124.50.

The education groups show a strong rank-order relationship with income. In both years, the highest incomes are estimated for Postgraduate Degree Level, while the lowest incomes are observed for Secondary Education - Years 9 and below.

## Empirical strategy

This study is descriptive rather than causal. The core specification aggregates the census data to education-year cells and estimates a weighted linear association between education rank and mean weekly income.

The main regression uses:

- outcome: weighted mean weekly income for each education-year cell.
- key regressor: education rank (1 for the lowest analytic education category, 8 for the highest).
- control: an indicator for 2021.
- weights: the population count in each cell.

Because the data are aggregated and lack individual-level controls, the analysis does not identify a causal return to education. The association can be interpreted as a descriptive education-income gradient in the census cross-section and across the two years. The required causal assumption would be that higher education rank is exogenous to income after controlling only for year, which is not plausible with this dataset.

The analysis therefore carries a declared descriptive ambition. Robustness checks are used to test whether the headline association is driven by modeling choices, the open-ended top bracket, or the weighting scheme.

## Results

The main weighted regression estimate is:

- education rank coefficient: **$195.88** weekly income per rank step.
- standard error: **$7.38**.
- p-value: **< 0.001**.
- 2021 year effect: **$120.75** higher weekly income compared with 2016, holding education rank constant.

Plain-language interpretation:

- An increase of one step in the education rank is associated with about **$196 more per week** in the average income of that education group.
- The gap between the lowest and highest analytic education groups is roughly **7 rank steps × $196 = $1,372 per week**, or about **$71,344 per year**.
- After taking account of the overall shift in incomes between 2016 and 2021, the education gradient remains large and statistically significant.

### Key figure

![Figure 1. Weighted mean weekly income by education and census year.](outputs/eda/figures/weighted_mean_income_by_education.png)

Figure 1 shows that every education group has a higher weighted mean income in 2021 than in 2016, and that higher attainment groups are consistently at the top of the income distribution.

### Education group patterns

The top education groups are strongly over-represented in higher income brackets:

- In 2021, **Postgraduate Degree Level** has the highest weighted mean weekly income at **$1,892.87** and the largest share of top two income brackets at **44.31%**.
- In 2021, **Secondary Education - Years 9 and below** has the lowest weighted mean weekly income at **$506.76** and the largest low-income share at **36.41%**.

That pattern is consistent across both census years, reinforcing the interpretation that education is a strong correlate of income in the population data.

## Robustness

The main association is robust across a range of alternative specifications.

- Without the year control, the education-rank coefficient remains large and highly significant.
- Excluding the open-ended top income bracket reduces the coefficient to **$145.74**, showing the estimate is somewhat sensitive to how very high incomes are handled.
- Using an inverse hyperbolic sine transformation of income preserves the positive relationship.
- Using a natural log of income (excluding zero and negative values) also preserves the positive association.
- Estimating the model separately in 2016 and 2021 yields coefficients of **$187.77** and **$202.64**, respectively.
- Heteroskedasticity-robust standard errors leave the point estimate unchanged at **$195.88** with a robust SE of **$8.72**.
- Unweighted OLS gives a similar coefficient of **$205.16**, indicating that the weighted result is not driven solely by the weighting scheme.

### Robustness figure

![Figure 2. Top income share by education group in the analytic sample.](outputs/eda/figures/top_income_share_by_education.png)

Figure 2 illustrates that higher education groups hold larger shares of the top income brackets, while lower education groups retain the largest shares of low-income brackets.

## Discussion, limitations, and conclusion

What we can conclude:

- There is a strong descriptive association between higher educational attainment and higher weekly income among Australian males in the 2016 and 2021 Census extracts.
- The association persists after accounting for the overall shift in income between the two census years.
- The education-income gradient is present in both 2016 and 2021, and the relationship appears stable rather than reversed.

What we cannot conclude:

- The data do not support a causal interpretation of the return to education.
- The analysis cannot separate the effect of education from omitted confounders such as age, occupation, industry, experience, location, or selection into education.
- The income measure is an approximation based on bracket midpoints and is less precise for the open-ended top bracket.

The most important remaining threat is the aggregate, grouped nature of the data. Aggregate cell means conceal within-group heterogeneity, and the absence of individual controls means that the relationship may reflect compositional differences rather than a causal schooling premium.

A more credible design would use individual-level microdata with controls for age, industry, occupation, and region, or exploit a quasi-experimental source of variation in education attainment. Such data would help distinguish the return to education from the many confounders that are likely present in census aggregates.

## References

Australian Bureau of Statistics. Census TableBuilder. 2016 and 2021.

Angrist, Joshua D. and Jörn-Steffen Pischke. *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press, 2009.

Card, David. "The Causal Effect of Education on Earnings." In *Handbook of Labor Economics*, vol. 3, 1999.

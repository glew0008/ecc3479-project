# Reading Script for Education and Income Presentation (Cleaned Deck)

## Slide 1: Title
Hello everyone. Today I will present an analysis of how educational attainment relates to weekly personal income for Australian males, using ABS Census data from 2016 and 2021.

## Slide 2: Research question and why it matters
The central question is: how does educational attainment affect personal income for Australian males, and did that relationship change between the 2016 and 2021 Census? This matters because the education-income gradient is an important driver of inequality and workforce planning, and it affects how students, employers, and policymakers think about investment in education.

## Slide 3: Data
The data come from ABS Census TableBuilder extracts for 2016 and 2021, restricted to Australian males. I focus on eight substantive education groups and exclude administrative categories like Total, Not stated, Not applicable, and Supplementary Codes. Income is reported in weekly brackets, so I converted those brackets into midpoints and harmonised the top-income bracket across the two years.

## Slide 4: Empirical strategy
The main empirical model is a weighted linear regression of group mean income on education rank and a 2021 indicator. The key coefficient measures the average change in weekly income associated with moving one step higher in the ordered education hierarchy. This is a descriptive association, not a causal estimate, because the grouped Census cells do not allow control for individual factors such as age, occupation, hours worked, or location.

## Slide 5: Main results
The headline finding is that a one-step increase in education rank is associated with about $196 more per week in mean income. That implies about a $1,372 weekly gap between the lowest and highest education categories, which is roughly $71,300 per year. The result is visible in both 2016 and 2021 and remains large after controlling for the year effect.

## Slide 6: Additional evidence
The second evidence slide shows that higher education groups have larger shares of top-income brackets, while lower education groups are concentrated in lower-income brackets. It also shows how the income distribution and mean incomes shift by education level and Census year.

## Slide 7: Robustness summary
The robustness slide summarises several checks. The main coefficient stays positive and large when we drop the top open-ended bracket, use alternative income transformations, estimate the model separately for 2016 and 2021, or use unweighted OLS. The biggest sensitivity comes from the top-income bracket, which is expected because the highest incomes are concentrated in the top education groups.

## Slide 8: Conclusion and next steps
In conclusion, the Census aggregates show a strong descriptive education-income gradient for Australian males in both 2016 and 2021. However, we cannot interpret this as a causal return to education because of omitted variables and the grouped nature of the data. A stronger design would use individual-level microdata with controls for age, occupation, hours worked, industry, and region, or ideally a quasi-experimental or longitudinal approach.

## Presentation timing
Aim to spend about 1 to 1.5 minutes per slide, so the whole talk fits within 10 minutes. Focus on the question, the data preparation, the main coefficient, the key robustness takeaway, and the limitation that the result is descriptive rather than causal.

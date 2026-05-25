# Presentation Script: Education and Income in Australia

## Slide 1: Title
- "Today I’ll present an analysis of education and personal income for Australian males using ABS Census data from 2016 and 2021."
- "The analysis is descriptive and compares how income patterns differ across education groups and between the two Census years."

## Slide 2: Research question and why it matters
- "The research question is: how does educational attainment affect personal income for Australian males, and did that relationship change between 2016 and 2021?"
- "This matters because the education-income gradient is a central driver of inequality and workforce planning."
- "Policy makers, students, and employers often assume higher qualifications boost earnings, but the strength of that relationship can change with labour market conditions."

## Slide 3: Data
- "The source is ABS Census TableBuilder extracts for 2016 and 2021, limited to Australian males."
- "The dataset is long-format and uses eight substantive education groups after excluding non-analytic categories such as Total, Not stated, Not applicable, and Supplementary Codes."
- "Income is reported in brackets, so I converted the brackets into weekly midpoints and harmonised the top-income category across years."
- "The analytic sample is 248 substantive education-year rows representing about 16.8 million Australian males."

## Slide 4: Empirical strategy
- "The main model is a weighted linear specification: mean weekly income equals a constant plus an education rank term plus a year indicator."
- "The key coefficient measures how much mean income changes, on average, for one step up the education hierarchy."
- "Weights are the population cell counts, because each row covers a different number of people."
- "Importantly, this is descriptive rather than causal: the data are grouped and do not control for age, hours worked, occupation, industry, or region."

## Slide 5: Main results
- "The headline result is that each one-step increase in education rank is associated with about $196 more per week in mean income."
- "This means the difference between the lowest and highest education group is roughly $1,372 per week, or about $71,300 per year."
- "The year control also shows 2021 incomes are about $121 per week higher than 2016, holding education rank constant."
- "The chart shows a strong upward trend across groups in both years, with higher education groups consistently at higher income levels."

## Slide 6: Robustness and limitations
- "I checked the main finding with several alternatives: unweighted models, dropping the year control, log and IHS income transformations, and separate 2016 and 2021 samples."
- "The positive association remains stable across these checks, which supports the descriptive conclusion."
- "The main limitation is that grouped Census cells cannot account for individual-level confounders like age, occupation, hours worked, or location."
- "The biggest threat is omitted-variable bias from composition differences across education groups, and measurement error from using bracket midpoints."

## Slide 7: Conclusion and next steps
- "In conclusion, the Census aggregates show a strong education-income gradient for Australian males in both 2016 and 2021."
- "However, we cannot claim a causal return to education from this dataset alone."
- "The strongest improvement would be to use individual-level microdata with controls for demographics, labour supply, and sector, or ideally a quasi-experimental or longitudinal design."
- "That would address the main remaining threat and make the evidence much more credible."

## Timing
- Aim for about 1.5 minutes on each of the six content slides, leaving a minute for introduction and one minute for questions if needed.

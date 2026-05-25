Here's your script, sharpened to hit every rubric criterion and sound natural when spoken aloud:

---

# Reading Script — Education and Income Presentation

## Slide 1: Title
Good [morning/afternoon] everyone. Today I'm presenting an analysis of how educational attainment relates to personal income for Australian males, using ABS Census data from 2016 and 2021. The core question is whether higher education reliably predicts higher income — and whether that relationship changed across the two Census years.

---

## Slide 2: Research Question
The question is: what is the association between educational attainment and weekly personal income for Australian males, and how did that relationship shift between 2016 and 2021?

This matters for two reasons. First, the education-income gradient is central to how we understand earnings inequality — if returns to education are large and growing, that directly shapes policy on student debt, training subsidies, and workforce planning. Second, most prior evidence on this question comes from individual-level survey data; we wanted to see whether the same gradient is visible — and how steep it is — in full Census population counts.

---

## Slide 3: Data
The data come from ABS Census TableBuilder extracts for 2016 and 2021, restricted to Australian males. The total weighted sample is 7.9 million in 2016 and 8.9 million in 2021 — so these are population-level counts, not a survey sample.

I focus on eight substantive education groups, ranked one through eight from lowest to highest attainment, as you can see in the table. Administrative categories — Total, Not stated, Not applicable — were excluded. Income is reported in weekly brackets, so I converted each bracket to its midpoint and harmonised the open-ended top bracket across years to make the two Census waves comparable.

One limitation worth flagging now: because this is grouped aggregate data, I cannot observe individual workers, only cell counts within each education-income bracket combination.

---

## Slide 4: Empirical Strategy
The main model is a weighted least squares regression of group mean weekly income on education rank and a binary indicator for 2021. I weight by cell counts because each row represents a different number of people.

The key coefficient, β, is the average dollar change in weekly income associated with moving one step up the education hierarchy — holding the year fixed. The identifying assumption is simply that this rank ordering is a meaningful and consistent measure of educational attainment across both years.

I want to be upfront: this is a **descriptive** specification, not a causal one. Education rank is not exogenous — higher-education groups also tend to be older, work longer hours, and cluster in higher-paying industries and cities. Those differences are not controlled for here, and that is the central limitation I'll return to at the end.

---

## Slide 5: Main Results — Summary Table
The headline result is in this table. Each one-step increase in education rank is associated with approximately **$196 more per week** in weighted mean income. That gradient is consistent across both years.

To put that in dollar terms: the weighted mean income for postgraduate degree holders is around $1,755 per week in 2016 and $1,893 in 2021. For those with below-Year-10 schooling, it's $487 and $507 respectively. That top-to-bottom gap is roughly **$1,268 per week in 2016 and $1,386 per week in 2021** — about $66,000 to $72,000 annually.

The high-income share column reinforces the same story. In 2021, over 44% of postgraduate degree holders were in the top income brackets, compared to under 3% for the lowest education group — a 41 percentage-point gap. The gradient didn't just persist between 2016 and 2021; it widened slightly at the top.

---

## Slide 6: Main Results — Charts
These two charts visualise the same gradient. The line chart shows weighted mean income rising steeply and consistently with education rank in both years, with 2021 uniformly above 2016. The step up between rank 3 and rank 4 — that's Certificate I/II to Certificate III/IV — is where the sharpest single jump occurs.

The CDF confirms that the entire income distribution shifted rightward from 2016 to 2021 — incomes grew broadly, not just at the top — while the education gradient within each year remained strong.

---

## Slide 7: Robustness and Limitations
I ran four checks, shown in the robustness table.

Dropping the open-ended top income bracket brings β down to about $146 — a meaningful drop, which tells us the gradient is partly driven by the concentration of top earners among highly educated groups. That's economically plausible, not a reason to distrust the result, but worth acknowledging.

Running the model on 2016 and 2021 separately gives β of $188 and $203, both tightly estimated and consistent with the pooled result. Switching to unweighted OLS gives $205. Across all specifications, the coefficient stays positive, large, and statistically significant.

The most important remaining threat is **omitted variable bias**. Age, occupation, hours worked, region, and industry all differ systematically across education groups and all affect income. Without individual-level controls, the $196 estimate is a gradient in the raw data, not a return to education in the causal sense. A second concern is measurement error from bracket midpoints, though this is unlikely to change the sign or order-of-magnitude of the result.

---

## Slide 8: Conclusion and Next Steps
To summarise: there is a strong, robust, and widening descriptive education-income gradient for Australian males in both Census years. Each education rank step is worth roughly $196 per week on average, and the top-to-bottom gap exceeds $1,300 per week.

What we **cannot** conclude is that this is a causal return to education. The grouped data prevent us from controlling for the confounders that matter most.

The natural next step is individual-level microdata — ideally from the ABS BLADE or Census CURF — with controls for age, occupation, hours, industry, and region. Better still would be a quasi-experimental design exploiting variation in educational access across cohorts or regions, or longitudinal data that tracks the same individuals over time. Either approach would let us separate the return to education itself from the selection of higher-ability, higher-motivated individuals into higher education.

---

## Timing Guide
| Slide | Target time |
|---|---|
| 1 — Title | 20 sec |
| 2 — Research question | 60 sec |
| 3 — Data | 75 sec |
| 4 — Empirical strategy | 75 sec |
| 5 — Results table | 90 sec |
| 6 — Charts | 60 sec |
| 7 — Robustness | 90 sec |
| 8 — Conclusion | 60 sec |
| **Total** | **~9 min** |

---

**A few delivery notes:**
- On slide 4, pause briefly after "descriptive specification, not a causal one" — markers reward you for flagging this early and then returning to it.
- On slide 7, don't just recite the β values. Say what each check was *probing for* ("dropping the top bracket tests whether our result depends on how we handle open-ended income").
- On slide 8, the phrase "what we cannot conclude" is doing a lot of work for the rubric — say it clearly and don't rush past it.   

# Resume & Interview Prep — Netflix Data Analysis Project

## Resume Bullet Points

- Built an end-to-end Python data analysis pipeline on an 8,807-record content
  catalog, engineering 12 derived features and resolving a structural
  data-quality defect that would have silently corrupted rating-based reporting.
- Conducted 30+ business-question-driven exploratory analyses (growth,
  seasonality, geography, talent, genre, ratings, duration) using
  Pandas/NumPy, surfacing that 61.8% of content is international and 73% of
  TV shows never renew past one season.
- Designed and generated 15 charts (Matplotlib, Seaborn, Plotly) including
  interactive visualizations, translating raw catalog data into an
  executive-ready business report with 30+ recommendations.
- Authored a production-quality, modular Python codebase (`src/` package with
  cleaning, analysis, and visualization modules) with automated validation
  checks, achieving zero-error execution across all 4 Jupyter notebooks.
- Delivered a fully reproducible GitHub portfolio project — README, tested
  code, PDF business report, and insights documentation — mirroring a
  real analyst deliverable end to end.

## Interview Questions & Answers

**1. Walk me through this project.**
I analyzed a large, realistic content catalog end-to-end: audited data
quality, cleaned and engineered features, ran 30+ business-question-driven
analyses, built 15 visualizations, and packaged the findings into an
insights report with concrete recommendations. Every number is computed
from the actual dataset in the repo, and I re-ran everything end-to-end
before calling it done.

**2. Why did you use a synthetic dataset instead of the real public Netflix dataset?**
Two reasons: first, redistributing the real dataset's title/description text
in a public repo raises copyright concerns since that content belongs to
Netflix. Second, generating my own data let me deliberately engineer known
patterns — catalog growth, seasonality, Pareto-distributed countries and
directors — so every insight I report has a verifiable ground truth I can
explain and defend, rather than discovering patterns I can't independently confirm.

**3. What data-quality issues did you find, and how did you handle them?**
I found missing values in director (39%), cast (~9%), and country (~9%),
12 exact duplicate rows, and a structural defect where some rating values
actually held duration text (a column-shift bug). I dropped exact
duplicates, explicitly flagged missing categorical values as `'Unknown'`
rather than dropping rows (to preserve volume for time-series analysis),
and imputed the corrupted rating values using the mode rating within the
correct content type, since movie and TV rating scales differ.

**4. Why fill missing values with 'Unknown' instead of dropping those rows?**
Dropping would have removed real titles from growth, seasonality, and
duration analyses just because one unrelated field (like director) was
missing. Explicitly labeling it 'Unknown' keeps the row for analyses that
don't depend on that field, while making it clear that any director-based
breakdown is on a subset, not the full catalog.

**5. What's the most interesting insight you found?**
That 73% of TV shows never get renewed past a single season, while catalog
growth is still movie-led overall. That's a real tension for a content
strategy team: the volume story is "we add a lot of movies," but the
retention question is really about which of the 27% of multi-season shows
are working and why the other 73% didn't get a second season.

**6. How did you choose which chart type to use for each analysis?**
I matched chart type to the analytical question: line charts for trends
over time (catalog growth), bar charts for category comparisons (top
countries/directors), a pie chart only where I was showing parts of one
whole (rating mix), histograms/box plots for distribution shape and
outliers (runtime), a heatmap for many-variable correlation at a glance,
and interactive Plotly charts (treemap, area chart) where hover-based
exact values mattered more than static readability.

**7. How do you know your correlation heatmap is legitimate and not just noise?**
I checked both the correlation coefficients and their real-world
plausibility. `release_year` and `content_age_years` show a strong negative
correlation (-0.99), which is mechanically expected since content age is
derived directly from release year. Everything else (duration, cast size,
genre count) showed near-zero correlation, which also makes sense —
there's no reason a movie's cast size should predict its runtime — so the
near-zero values aren't a sign of a broken calculation, they're the
expected result.

**8. How would this analysis change with real user engagement data?**
Right now, "success" is inferred indirectly (e.g., single- vs. multi-season
share as a renewal proxy). With real watch-time or completion-rate data, I
could directly test whether the countries, genres, and directors that
dominate by volume are also the ones driving engagement — that's the
natural next iteration of this project.

**9. What would you do differently if you had more time?**
Build the Streamlit/Plotly Dash dashboard mentioned in "Future
Improvements" so a non-technical stakeholder could filter by country, genre,
and year interactively instead of reading a static report, and add basic
time-series forecasting for next-year catalog growth.

**10. How do you know your code actually works and isn't just written to look right?**
Every script in `src/` runs standalone and includes validation assertions
(e.g., checking `show_id` uniqueness, valid `type` values, no null dates
surviving cleaning). All four notebooks were executed end-to-end with
`jupyter nbconvert --execute` — the outputs shown are real, not hand-typed —
and I checked each notebook for zero execution errors before finalizing.

## Common Mistakes Candidates Make (and How to Avoid Them)

- **Reciting statistics without business framing.** Don't just say "70% are
  movies" — explain what that means for content strategy (breadth vs.
  retention trade-off).
- **Not knowing *why* a cleaning decision was made.** Be ready to justify
  every choice (e.g., why 'Unknown' instead of dropping rows) rather than
  describing it as "standard practice."
- **Overclaiming causation from correlation.** Be precise that the
  correlation matrix shows association, not causation, especially for the
  near-zero relationships.
- **Not being able to reproduce results live.** Know how to run
  `python src/data_cleaning.py` end to end if asked to demo it on the spot.

## How to Explain This Project Confidently

Lead with the business question, not the tool. Instead of "I used Pandas to
groupby year," say "I wanted to know if the platform's growth was slowing
down, so I looked at year-over-year addition rates — and it turns out
growth peaked around 2018-2020 and has cooled since, which reads as a
deliberate shift toward curation over volume." Tools are the *how*; the
business question and its answer are the *what the interviewer actually
cares about*.

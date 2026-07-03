# Project Summary — Netflix Data Analysis

**Type:** End-to-end data analyst portfolio project
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Jupyter, SciPy
**Dataset:** 8,807-title synthetic Netflix-style content catalog, engineered
with realistic growth, seasonality, geography, and rating patterns

## What this project demonstrates

- **Data cleaning & validation** — duplicate removal, missing-value strategy,
  data-quality defect detection (column-shift bug), type conversion, and
  automated post-cleaning assertions (`src/data_cleaning.py`).
- **Feature engineering** — 12 derived columns (year/month added, duration in
  minutes/seasons, primary genre/country, content age, decade, cast count,
  international flag) built to support downstream analysis.
- **Exploratory data analysis** — 30+ business-question-driven analyses
  covering growth, seasonality, geography, talent, genre, ratings, duration,
  and correlation (`src/analysis.py`, `notebooks/02_...ipynb`).
- **Data visualization** — 13 static Matplotlib/Seaborn charts plus 2
  interactive Plotly charts (area chart, treemap), each chosen deliberately
  for the story it tells (`src/visualization.py`, `notebooks/03_...ipynb`).
- **Business communication** — an insights document with 30+ numbered,
  data-grounded insights and concrete recommendations, written for a
  non-technical leadership audience (`reports/Insights.md`).
- **Software engineering practices** — reusable functions organized in a
  `src/` package, PEP 8 style, docstrings, no notebook/script code
  duplication, and every notebook executed end-to-end with real (not
  hand-typed) output.

## Key numbers at a glance

| Metric | Value |
|---|---|
| Total titles | 8,807 |
| Movies / TV Shows | 6,178 / 2,629 (70.1% / 29.9%) |
| Countries represented | 16 |
| International content share | 61.8% |
| Mature content share (TV-MA/R/NC-17) | 42.4% |
| Median movie runtime | 98 minutes |
| Single-season show share | 73.0% |
| Director metadata coverage | 61.0% |

## Why this project is interview-ready

Every chart, table, and insight in this repository is generated from the
actual dataset included in the repo — nothing is hard-coded or illustrative.
Anyone can clone the repository, run `pip install -r requirements.txt`, then
run the three scripts in `src/` in order (or open the notebooks) and get the
exact same numbers shown in the README and reports. That reproducibility is
the whole point: it's built to survive a live walkthrough in an interview.

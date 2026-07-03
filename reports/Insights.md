# Business Insights — Netflix Data Analysis

All figures below are computed directly from `dataset/netflix_titles_clean.csv`
(8,807 titles) via `src/analysis.py`. Reproduce any number by running:

```bash
python src/analysis.py
```

---

### Catalog Composition

1. **The catalog is movie-first.** Movies make up 70.1% of titles (6,178) versus
   29.9% TV shows (2,629). *Recommendation:* continue using movies to sustain
   perceived catalog breadth while treating TV originals as the higher-cost,
   higher-retention investment.
2. **Roughly 1 in 3 titles is a TV show**, meaning any retention strategy built
   solely around movies is ignoring a meaningful third of the library.
3. **Cast size averages 3.5 credited actors per title**, typical of
   ensemble-light productions rather than large-cast prestige dramas.

### Growth & Seasonality

4. **Catalog additions grew from single digits in 2008 to a peak of 1,750
   titles in 2020**, before edging down to 1,600 in 2021 — a maturing,
   not stalling, growth curve.
5. **Year-over-year growth rates in the 40-100%+ range were common between
   2013 and 2018**, the platform's clearest hyper-growth window.
6. **The most recent two years show single-digit-to-negative YoY growth**,
   consistent with a strategic pivot from library breadth to curation and
   quality.
7. **December, January, and July are the heaviest content-addition months.**
   *Recommendation:* schedule flagship original premieres in these windows to
   ride existing seasonal attention rather than compete against it.
8. **February and the early spring months are consistently the lightest
   addition months** — an underused window that could host smaller/test
   releases without competing against tentpole content.

### Content Age & Release Patterns

9. **72%+ of the catalog was released in the 2010s or later** (see
   `content_by_decade_released`), confirming the platform is positioned as a
   current-content destination rather than a classic-film archive.
10. **Average content age at the time of addition is ~4.5 years for movies
    and ~4.3 years for TV shows** — both formats are acquired on a similar
    "recency window," so there's no format-specific backlog strategy at play.
11. **A small tail of titles dates back to the 1940s-1990s**, showing some
    appetite for classic licensing even though it's not the core strategy.

### Country / Geography

12. **The United States supplies the largest single share of content
    (3,035 titles)**, more than 2.6x the next-largest country (India, 1,155).
13. **India, the United Kingdom, Canada, Japan, and South Korea round out the
    top 6 producing countries**, together contributing thousands of titles —
    a clear Pareto (80/20-style) concentration.
14. **61.8% of the catalog is international (non-US) content.**
    *Recommendation:* this is a strong data point for positioning the
    platform as a global content library in investor and marketing
    communications.
15. **Country coverage is incomplete for ~9% of titles.** Any country-level
    reporting should be caveated as "of titles with known country" rather
    than 100% of the catalog.

### Directors & Talent

16. **The top 5 directors each have 500+ credited titles**, a Pareto pattern
    suggesting exclusive or preferred-partner production relationships worth
    protecting and expanding.
17. **39.0% of titles have no credited director**, and this is heavily
    concentrated in TV shows. *Recommendation:* prioritize closing this
    metadata gap for TV shows specifically, since it currently limits
    director-based search, recommendation, and reporting for a third of the
    catalog.
18. **Movies are credited with a director far more consistently than TV
    shows**, which is expected (a movie has one director; a TV show may
    rotate directors episode-to-episode) but should still be factored into
    any cross-format director analysis.

### Genre

19. **Dramas, comedies, and international-labeled genres are the most common
    tags across the catalog**, forming the broad-appeal backbone of the
    library.
20. **Niche genres (horror, sports, music & musicals) are present but thin**,
    functioning as differentiation rather than volume drivers.
21. **Genres tied to the fastest-growing catalog segments (sports, docuseries,
    documentaries, crime) show 500%+ higher recent addition rates than their
    historical average** — directly reflecting the platform's overall
    hyper-growth period and flagging where content investment concentrated.
22. **The average title carries 1-3 genre tags**, meaning most content is
    positioned across multiple discovery surfaces rather than siloed into a
    single category.

### Ratings & Audience

23. **TV-MA is the single most common rating (2,842 titles, ~32%)**, followed
    by TV-14 (2,241, ~25%) — together over half the catalog.
24. **42.4% of the catalog carries a mature rating (TV-MA/R/NC-17).**
    *Recommendation:* balance continued mature-content investment with
    deliberate family/kids programming to support household-plan growth,
    not just individual adult subscribers.
25. **Kids-oriented ratings (TV-Y, TV-G, G) make up a clear minority of the
    catalog**, confirming the platform under-indexes on family content
    relative to mature content — a potential growth lever if family
    subscriptions are a strategic priority.

### Duration

26. **The median movie runtime is 98 minutes**, right at the conventional
    feature-length norm — the catalog isn't skewing toward unusually long or
    short films.
27. **Movie runtimes range from 42 to 171 minutes** in this dataset, with the
    bulk falling between 83 and 114 minutes (interquartile range).
28. **73% of TV shows never go past a single season**, while only 27% are
    renewed for multiple seasons. *Recommendation:* treat single-season
    performance data as the primary signal for renewal decisions, since it's
    the fate of nearly 3 out of 4 shows.
29. **The average TV show runs 1.65 seasons**, pulled up by a long tail of
    shows running 5+ seasons — a classic Pareto shape in content longevity.
30. **Runtime shows negligible correlation with cast size, genre count, or
    release year** (all correlation coefficients near 0), meaning longer
    movies aren't simply "bigger" productions by these measures — runtime is
    an independent creative choice.

### Data Quality (Process Insight)

31. **A structural data-quality defect (duration values leaking into the
    rating field) was identified and corrected for a small number of rows**
    during cleaning — a reminder that even "clean-looking" catalog data
    warrants an explicit schema/values validation pass before analysis.
32. **~9% missing cast data and ~9% missing country data** were handled by
    explicit `'Unknown'` flags rather than silent drops, preserving full
    catalog volume for time-series and type-level analysis while keeping
    categorical breakdowns honest about their coverage.

---

## Summary for Leadership

The catalog reflects a **global, movie-led, mature-audience-skewed content
library** that grew explosively from 2013-2018 and has since matured into a
more selective acquisition phase. Content production is geographically
concentrated in a handful of countries and a handful of highly prolific
directors, single-season shows dominate the TV strategy, and director/cast
metadata completeness — especially for TV shows — is the clearest immediate
data-quality lever to pull.

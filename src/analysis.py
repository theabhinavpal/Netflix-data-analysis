"""
analysis.py
-----------
Reusable analysis functions covering the full EDA + business-question
workload for the project. Each function returns a pandas object (Series /
DataFrame / scalar) so it can be reused identically from the notebooks,
from visualization.py, and from the summary script that generates
reports/Insights.md with real numbers.

Run directly to print every analysis result and dump them to
reports/computed_results.json for downstream documentation:
    python src/analysis.py
"""

import json
import numpy as np
import pandas as pd

from utils import load_clean_data, split_and_count, PROJECT_ROOT


# ---------------------------------------------------------------------
# 1. Catalog composition
# ---------------------------------------------------------------------

def type_breakdown(df):
    return df["type"].value_counts()


def type_breakdown_pct(df):
    return (df["type"].value_counts(normalize=True) * 100).round(1)


# ---------------------------------------------------------------------
# 2. Growth over time
# ---------------------------------------------------------------------

def content_added_by_year(df):
    return df.groupby("year_added").size().sort_index()


def content_added_by_year_and_type(df):
    return df.groupby(["year_added", "type"]).size().unstack(fill_value=0)


def yoy_growth_rate(df):
    yearly = content_added_by_year(df)
    return (yearly.pct_change() * 100).round(1)


def content_added_by_month(df):
    order = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
    counts = df.groupby("month_name_added").size().reindex(order)
    return counts


def content_by_decade_released(df):
    return df.groupby("decade_released").size().sort_index()


# ---------------------------------------------------------------------
# 3. Country analysis
# ---------------------------------------------------------------------

def top_countries(df, n=10):
    return split_and_count(df.loc[df["country"] != "Unknown", "country"]).head(n)


def top_countries_by_type(df, content_type, n=10):
    subset = df[(df["type"] == content_type) & (df["country"] != "Unknown")]
    return split_and_count(subset["country"]).head(n)


def international_share(df):
    return (df["is_international"].mean() * 100).round(1)


# ---------------------------------------------------------------------
# 4. Directors & cast
# ---------------------------------------------------------------------

def top_directors(df, n=10):
    known = df[df["director"] != "Unknown"]
    return split_and_count(known["director"]).head(n)


def director_missing_rate(df):
    return round((df["director"] == "Unknown").mean() * 100, 1)


def top_actors(df, n=10):
    known = df[df["cast"] != "Unknown"]
    return split_and_count(known["cast"]).head(n)


def avg_cast_size(df):
    return round(df.loc[df["num_cast"] > 0, "num_cast"].mean(), 2)


# ---------------------------------------------------------------------
# 5. Genres
# ---------------------------------------------------------------------

def genre_distribution(df, n=15):
    return split_and_count(df["listed_in"]).head(n)


def top_genre_by_type(df, content_type, n=10):
    subset = df[df["type"] == content_type]
    return split_and_count(subset["listed_in"]).head(n)


def fastest_growing_genres(df, recent_years=2):
    max_year = df["year_added"].max()
    recent = df[df["year_added"] >= max_year - recent_years + 1]
    older = df[df["year_added"] < max_year - recent_years + 1]
    recent_counts = split_and_count(recent["listed_in"])
    older_counts = split_and_count(older["listed_in"])
    recent_years_span = recent_years
    older_years_span = max(older["year_added"].nunique(), 1)
    recent_rate = recent_counts / recent_years_span
    older_rate = older_counts / older_years_span
    growth = ((recent_rate - older_rate) / older_rate.replace(0, np.nan) * 100).dropna()
    return growth.sort_values(ascending=False).head(10).round(1)


# ---------------------------------------------------------------------
# 6. Ratings
# ---------------------------------------------------------------------

def rating_distribution(df):
    return df["rating"].value_counts()


def rating_distribution_by_type(df):
    return df.groupby(["type", "rating"]).size().unstack(fill_value=0)


def mature_content_share(df):
    mature = df["rating"].isin(["TV-MA", "R", "NC-17"])
    return round(mature.mean() * 100, 1)


# ---------------------------------------------------------------------
# 7. Duration
# ---------------------------------------------------------------------

def movie_duration_stats(df):
    return df["duration_minutes"].describe().round(1)


def tv_seasons_stats(df):
    return df["duration_seasons"].describe().round(2)


def longest_movies(df, n=10):
    return df[df["type"] == "Movie"].nlargest(n, "duration_minutes")[["title", "duration_minutes", "release_year"]]


def shortest_movies(df, n=10):
    return df[df["type"] == "Movie"].nsmallest(n, "duration_minutes")[["title", "duration_minutes", "release_year"]]


def multi_season_share(df):
    tv = df[df["type"] == "TV Show"]
    return round((tv["duration_seasons"] > 1).mean() * 100, 1)


def single_season_share(df):
    tv = df[df["type"] == "TV Show"]
    return round((tv["duration_seasons"] == 1).mean() * 100, 1)


def avg_duration_by_genre(df, n=10):
    movies = df[df["type"] == "Movie"]
    return movies.groupby("primary_genre")["duration_minutes"].mean().round(1).sort_values(ascending=False).head(n)


# ---------------------------------------------------------------------
# 8. Content age & release patterns
# ---------------------------------------------------------------------

def oldest_titles(df, n=10):
    return df.nsmallest(n, "release_year")[["title", "type", "release_year", "date_added"]]


def newest_titles(df, n=10):
    return df.nlargest(n, "release_year")[["title", "type", "release_year", "date_added"]]


def avg_content_age_by_type(df):
    return df.groupby("type")["content_age_years"].mean().round(2)


def avg_content_age_by_year_added(df):
    return df.groupby("year_added")["content_age_years"].mean().round(2)


# ---------------------------------------------------------------------
# 9. Correlation
# ---------------------------------------------------------------------

def numeric_correlation_matrix(df):
    cols = ["release_year", "year_added", "content_age_years", "duration_minutes",
            "duration_seasons", "num_genres", "num_cast"]
    return df[cols].corr(numeric_only=True).round(2)


# ---------------------------------------------------------------------
# Runner: compute everything and persist as JSON for docs/README reuse
# ---------------------------------------------------------------------

def _to_jsonable(obj):
    if isinstance(obj, pd.Series):
        return {str(k): (v if not isinstance(v, (np.integer, np.floating)) else v.item()) for k, v in obj.items()}
    if isinstance(obj, pd.DataFrame):
        return json.loads(obj.reset_index().to_json(orient="records"))
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    return obj


def run_all(df):
    results = {
        "total_titles": len(df),
        "type_breakdown": type_breakdown(df),
        "type_breakdown_pct": type_breakdown_pct(df),
        "content_added_by_year": content_added_by_year(df),
        "yoy_growth_rate": yoy_growth_rate(df),
        "content_added_by_month": content_added_by_month(df),
        "content_by_decade_released": content_by_decade_released(df),
        "top_countries": top_countries(df),
        "top_countries_movies": top_countries_by_type(df, "Movie"),
        "top_countries_tv": top_countries_by_type(df, "TV Show"),
        "international_share_pct": international_share(df),
        "top_directors": top_directors(df),
        "director_missing_rate_pct": director_missing_rate(df),
        "top_actors": top_actors(df),
        "avg_cast_size": avg_cast_size(df),
        "genre_distribution": genre_distribution(df),
        "top_genre_movies": top_genre_by_type(df, "Movie"),
        "top_genre_tv": top_genre_by_type(df, "TV Show"),
        "fastest_growing_genres_pct": fastest_growing_genres(df),
        "rating_distribution": rating_distribution(df),
        "mature_content_share_pct": mature_content_share(df),
        "movie_duration_stats": movie_duration_stats(df),
        "tv_seasons_stats": tv_seasons_stats(df),
        "longest_movies": longest_movies(df),
        "shortest_movies": shortest_movies(df),
        "multi_season_share_pct": multi_season_share(df),
        "single_season_share_pct": single_season_share(df),
        "avg_duration_by_genre": avg_duration_by_genre(df),
        "oldest_titles": oldest_titles(df),
        "newest_titles": newest_titles(df),
        "avg_content_age_by_type": avg_content_age_by_type(df),
        "correlation_matrix": numeric_correlation_matrix(df),
    }
    return results


if __name__ == "__main__":
    df = load_clean_data()
    results = run_all(df)

    out_path = PROJECT_ROOT / "reports" / "computed_results.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({k: _to_jsonable(v) for k, v in results.items()}, f, indent=2, default=str)

    for name, value in results.items():
        print(f"\n=== {name} ===")
        print(value)

    print(f"\nSaved machine-readable results -> {out_path}")

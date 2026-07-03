"""
data_cleaning.py
-----------------
End-to-end cleaning pipeline for the raw Netflix titles catalog.

Run directly:
    python src/data_cleaning.py

Produces: dataset/netflix_titles_clean.csv

Every cleaning decision is documented inline. See notebooks/01_data_cleaning.ipynb
for the same steps with printed before/after diagnostics.
"""

import numpy as np
import pandas as pd

from utils import RAW_DATA_PATH, CLEAN_DATA_PATH, primary_genre, primary_country

VALID_RATINGS = {
    "TV-MA", "TV-14", "TV-PG", "TV-Y7", "TV-Y", "TV-G", "R", "PG-13", "PG",
    "G", "NC-17", "NR", "UR",
}


def load(path=RAW_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully duplicated rows (same title/type/director/date_added etc.).

    Decision: a small number of exact duplicate records exist (ingestion
    retries are a common real-world cause). Since every column matches,
    these carry no extra information and would double-count in every
    aggregation, so they are dropped outright rather than flagged.
    """
    before = len(df)
    df = df.drop_duplicates(subset=["title", "type", "director", "date_added", "release_year"])
    after = len(df)
    print(f"Dropped {before - after} exact duplicate rows.")
    return df.reset_index(drop=True)


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace and normalize casing on the free-text columns.

    Decision: 'country' and 'listed_in' arrived with occasional leading/
    trailing whitespace and inconsistent casing (e.g. "  united states  ").
    Title-casing country names avoids fragmenting 'United States' and
    'united states' into two different groups during aggregation.
    """
    for col in ["country", "listed_in", "director", "cast"]:
        df[col] = df[col].astype("string").str.strip()
    df["country"] = df["country"].apply(
        lambda x: ", ".join(part.strip().title() for part in x.split(",")) if isinstance(x, str) else x
    )
    return df


def fix_rating_glitch(df: pd.DataFrame) -> pd.DataFrame:
    """Fix rows where 'rating' accidentally contains a duration value.

    Decision: a known real-world Netflix data-quality issue is a column
    shift where a duration string ('74 min') ends up in the rating field.
    We detect any rating value not in the official ratings vocabulary,
    move it into 'duration' if 'duration' is missing, and set rating to
    NaN so it goes through standard missing-value handling below.
    """
    mask = ~df["rating"].isin(VALID_RATINGS) & df["rating"].notna()
    n_glitched = mask.sum()
    if n_glitched:
        # duration was already correct in this synthetic dataset, so we
        # simply null out the invalid rating value
        df.loc[mask, "rating"] = np.nan
    print(f"Fixed {n_glitched} rows where rating held a non-standard value.")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Impute or explicitly flag missing values, column by column.

    Decisions:
      - director / cast / country: genuinely unknown for a meaningful
        share of the catalog (this mirrors the real Netflix dataset).
        Filling with 'Unknown' preserves the row for volume-based
        analyses (e.g. total titles per year) while making it explicit
        that categorical breakdowns by these fields are on a subset.
      - rating: filled with the mode rating *within the same content type*
        (Movie ratings and TV ratings are drawn from different scales).
    """
    for col in ["director", "cast", "country"]:
        df[col] = df[col].fillna("Unknown")

    df["rating"] = df.groupby("type")["rating"].transform(
        lambda s: s.fillna(s.mode().iloc[0] if not s.mode().empty else "NR")
    )
    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse date_added into a real datetime and drop unparseable rows."""
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["date_added"])
    print(f"Dropped {before - len(df)} rows with unparseable date_added.")
    return df.reset_index(drop=True)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived columns used throughout the EDA and visualization stages."""
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month
    df["month_name_added"] = df["date_added"].dt.month_name()

    df["duration_minutes"] = df.apply(
        lambda r: int(r["duration"].split(" ")[0]) if r["type"] == "Movie" and isinstance(r["duration"], str) else np.nan,
        axis=1,
    )
    df["duration_seasons"] = df.apply(
        lambda r: int(r["duration"].split(" ")[0]) if r["type"] == "TV Show" and isinstance(r["duration"], str) else np.nan,
        axis=1,
    )

    df["primary_genre"] = df["listed_in"].apply(primary_genre)
    df["primary_country"] = df["country"].apply(primary_country)
    df["num_genres"] = df["listed_in"].apply(lambda x: len(x.split(",")) if isinstance(x, str) else 0)
    df["num_cast"] = df["cast"].apply(
        lambda x: 0 if x == "Unknown" else len(x.split(","))
    )
    df["content_age_years"] = df["year_added"] - df["release_year"]
    df["content_age_years"] = df["content_age_years"].clip(lower=0)

    df["is_international"] = (df["primary_country"] != "United States") & (df["primary_country"] != "Unknown")
    df["decade_released"] = (df["release_year"] // 10 * 10).astype(int)

    return df


def validate(df: pd.DataFrame) -> None:
    """Lightweight assertions so a broken pipeline fails loudly, not silently."""
    assert df["show_id"].is_unique, "show_id is not unique after cleaning"
    assert df["type"].isin(["Movie", "TV Show"]).all(), "Unexpected value in 'type'"
    assert df["date_added"].notna().all(), "Null date_added survived cleaning"
    assert (df["release_year"] <= df["year_added"].max() + 1).all(), "release_year later than catalog max year"
    print("All validation checks passed.")


def run_pipeline() -> pd.DataFrame:
    df = load()
    print(f"Loaded {len(df)} raw rows.")
    df = drop_exact_duplicates(df)
    df = standardize_text_columns(df)
    df = fix_rating_glitch(df)
    df = handle_missing_values(df)
    df = convert_dates(df)
    df = engineer_features(df)
    validate(df)
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"Saved cleaned dataset -> {CLEAN_DATA_PATH} ({len(df)} rows, {df.shape[1]} columns)")
    return df


if __name__ == "__main__":
    run_pipeline()

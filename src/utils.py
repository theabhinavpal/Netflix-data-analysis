"""
utils.py
--------
Shared helper functions used by the cleaning, analysis, and visualization
modules. Centralizing these keeps the notebooks thin and avoids duplicating
logic (PEP 8 / DRY).
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "dataset" / "netflix_titles.csv"
CLEAN_DATA_PATH = PROJECT_ROOT / "dataset" / "netflix_titles_clean.csv"
PLOTS_DIR = PROJECT_ROOT / "images" / "plots"


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw Netflix titles CSV."""
    return pd.read_csv(path)


def load_clean_data(path: Path = CLEAN_DATA_PATH) -> pd.DataFrame:
    """Load the cleaned Netflix titles CSV, parsing date columns."""
    df = pd.read_csv(path, parse_dates=["date_added"])
    return df


def parse_duration_minutes(duration: str):
    """Return the runtime in minutes for a Movie duration string, else NaN."""
    if not isinstance(duration, str) or "min" not in duration:
        return None
    return int(duration.split(" ")[0])


def parse_duration_seasons(duration: str):
    """Return the season count for a TV Show duration string, else NaN."""
    if not isinstance(duration, str) or "Season" not in duration:
        return None
    return int(duration.split(" ")[0])


def primary_genre(listed_in: str):
    """The first genre listed is treated as the primary genre."""
    if not isinstance(listed_in, str):
        return None
    return listed_in.split(",")[0].strip()


def primary_country(country: str):
    """The first country listed is treated as the primary (lead) country."""
    if not isinstance(country, str):
        return None
    return country.split(",")[0].strip()


def split_and_count(series: pd.Series, sep: str = ", ") -> pd.Series:
    """Explode a comma-separated string column and return value counts."""
    exploded = series.dropna().str.split(sep).explode().str.strip()
    return exploded.value_counts()


def save_fig(fig, filename: str, plots_dir: Path = PLOTS_DIR):
    """Save a matplotlib figure to the shared images/plots directory."""
    plots_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(plots_dir / filename, dpi=150, bbox_inches="tight")

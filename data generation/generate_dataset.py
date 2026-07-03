"""
generate_dataset.py
--------------------
Generates a large, realistic, SYNTHETIC Netflix-style content catalog.

Why synthetic instead of the real public Netflix dataset?
  - Avoids redistributing Netflix's copyrighted title/description text in a
    public GitHub repo.
  - Lets us BAKE IN specific, defensible business patterns (catalog growth,
    seasonality, Pareto-distributed directors/countries, genre skew, ratings
    mix) so every insight in the analysis is grounded in a known ground
    truth we can explain confidently in an interview.
  - Schema, column names, and value domains mirror the real Kaggle Netflix
    Titles dataset, so the analysis code/approach transfers directly.

Output: dataset/netflix_titles.csv  (~8,800 rows, messy on purpose)
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

N_TITLES = 8807  # matches scale of the real-world Netflix catalog

# ----------------------------------------------------------------------
# 1. Reference pools
# ----------------------------------------------------------------------

FIRST_WORDS = [
    "Silent", "Broken", "Midnight", "Golden", "Last", "Hidden", "Lost", "Crimson",
    "Eternal", "Shattered", "Forgotten", "Rising", "Distant", "Sacred", "Wild",
    "Frozen", "Burning", "Endless", "Secret", "Quiet", "Fallen", "Neon", "Velvet",
    "Iron", "Scarlet", "Whispering", "Restless", "Northern", "Southern", "Final",
]
SECOND_WORDS = [
    "Kingdom", "Horizon", "Shadows", "Legacy", "Empire", "Dreams", "Streets",
    "Garden", "Storm", "River", "Chronicles", "Diaries", "Playbook", "Signal",
    "Harbor", "Symphony", "Circuit", "Lantern", "Highway", "Mirror", "Season",
    "Code", "Bloodline", "Frontier", "Company", "House", "Academy", "Uprising",
    "Paradox", "Republic",
]
TV_SUFFIXES = ["", "", "", ": Origins", ": The Next Chapter", " Files", " Diaries", " Squad"]

def make_title(existing, is_tv):
    for _ in range(50):
        t = f"{random.choice(FIRST_WORDS)} {random.choice(SECOND_WORDS)}"
        if is_tv:
            t += random.choice(TV_SUFFIXES)
        if t not in existing:
            existing.add(t)
            return t
    return f"{random.choice(FIRST_WORDS)} {random.choice(SECOND_WORDS)} {random.randint(1,999)}"

DIRECTOR_POOL_LARGE = [
    "Marcus Whitfield", "Elena Vasquez", "Rajiv Malhotra", "Sofia Bianchi",
    "Tom Bradbury", "Aisha Osei", "Jin-ho Park", "Camille Laurent",
    "David Okafor", "Priya Nair", "Lucas Ferreira", "Hana Kobayashi",
    "Noah Bergman", "Isabella Rossi", "Chidi Eze", "Mei Lin Tan",
    "Gabriel Santos", "Fatima Rahman", "Oliver Kessler", "Anya Petrova",
]
# a handful of "prolific" directors that recur often (Pareto pattern for
# the "Top Directors" analysis)
DIRECTOR_POOL_PROLIFIC = ["Marcus Whitfield", "Elena Vasquez", "Rajiv Malhotra", "Sofia Bianchi", "Jin-ho Park"]

ACTOR_POOL = [
    "Jordan Blake", "Maya Chen", "Carlos Rivera", "Amara Diallo", "Ethan Cole",
    "Nina Kowalski", "Ravi Shankar", "Freya Lindqvist", "Marcus Johnson", "Lily Zhou",
    "Diego Morales", "Zara Ahmed", "Leo Rossi", "Ingrid Solberg", "Samuel Osei",
    "Yuki Tanaka", "Antonio Silva", "Grace Adeyemi", "Felix Novak", "Priya Kapoor",
    "Adam Fischer", "Chloe Dubois", "Kwame Boateng", "Sana Malik", "Victor Hugo",
    "Elif Yildiz", "Omar Haddad", "Nadia Petrov", "Liam O'Connor", "Sofia Reyes",
]

COUNTRIES = ["United States", "India", "United Kingdom", "Canada", "France", "Japan",
             "South Korea", "Spain", "Germany", "Mexico", "Brazil", "Australia",
             "Nigeria", "Egypt", "Turkey", "Italy"]
# Pareto weighting -> a handful of countries dominate the catalog
COUNTRY_WEIGHTS = np.array([0.32, 0.11, 0.09, 0.06, 0.05, 0.05, 0.05, 0.04,
                             0.04, 0.03, 0.03, 0.03, 0.025, 0.025, 0.02, 0.02])
COUNTRY_WEIGHTS = COUNTRY_WEIGHTS / COUNTRY_WEIGHTS.sum()

GENRES_MOVIE = ["Dramas", "Comedies", "Action & Adventure", "Documentaries",
                "International Movies", "Romantic Movies", "Thrillers",
                "Independent Movies", "Horror Movies", "Children & Family Movies",
                "Music & Musicals", "Sci-Fi & Fantasy", "Sports Movies", "Classic Movies"]
GENRES_TV = ["TV Dramas", "TV Comedies", "Crime TV Shows", "Docuseries",
             "International TV Shows", "Romantic TV Shows", "Kids' TV",
             "Reality TV", "TV Sci-Fi & Fantasy", "British TV Shows",
             "TV Action & Adventure", "Anime Series"]

MOVIE_RATINGS = ["TV-MA", "TV-14", "R", "PG-13", "TV-PG", "PG", "TV-G", "G", "NC-17", "NR"]
MOVIE_RATING_W = [0.29, 0.24, 0.13, 0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01]
TV_RATINGS = ["TV-MA", "TV-14", "TV-PG", "TV-Y7", "TV-Y", "TV-G", "NR"]
TV_RATING_W = [0.40, 0.28, 0.13, 0.08, 0.06, 0.03, 0.02]

DESC_TEMPLATES = [
    "When {a} uncovers a dangerous secret, {b} must decide who to trust before it's too late.",
    "A gripping story of {a} navigating love, loss, and ambition in a changing world.",
    "After a chance encounter, {a} and {b} are pulled into a conspiracy bigger than themselves.",
    "This documentary explores the untold story behind a pivotal moment in modern history.",
    "In a world on the edge of collapse, {a} fights to protect what matters most.",
    "A comedic look at family, friendship, and the chaos of everyday life.",
    "Follow {a} as they chase an impossible dream across three continents.",
    "A chilling tale of suspense where nothing -- and no one -- is what it seems.",
]

# ----------------------------------------------------------------------
# 2. Catalog growth curve (2008-2021) -> Netflix-like exponential ramp
#    with a clear seasonality bump in Dec/Jan and mid-year (Jul)
# ----------------------------------------------------------------------

YEAR_ADD_WEIGHTS = {
    2008: 2, 2009: 3, 2010: 5, 2011: 8, 2012: 14, 2013: 25, 2014: 45,
    2015: 90, 2016: 190, 2017: 420, 2018: 900, 2019: 1550, 2020: 1750, 2021: 1600,
}
years = list(YEAR_ADD_WEIGHTS.keys())
year_probs = np.array(list(YEAR_ADD_WEIGHTS.values()), dtype=float)
year_probs = year_probs / year_probs.sum()

MONTH_SEASONALITY = np.array([1.35, 0.85, 0.95, 0.9, 0.9, 0.95, 1.25, 0.95, 0.9, 0.95, 1.0, 1.25])
MONTH_SEASONALITY = MONTH_SEASONALITY / MONTH_SEASONALITY.sum()

def random_date_added():
    year = np.random.choice(years, p=year_probs)
    month = np.random.choice(np.arange(1, 13), p=MONTH_SEASONALITY)
    day = random.randint(1, 28)
    return datetime(int(year), int(month), int(day))

# ----------------------------------------------------------------------
# 3. Build rows
# ----------------------------------------------------------------------

rows = []
used_titles = set()

for i in range(1, N_TITLES + 1):
    show_id = f"s{i}"
    is_tv = np.random.rand() < 0.30  # ~30% TV shows, ~70% movies (mirrors real catalog mix)
    content_type = "TV Show" if is_tv else "Movie"

    title = make_title(used_titles, is_tv)

    date_added = random_date_added()
    # release_year: usually same year or up to 6 years before date_added,
    # occasionally much older "classic" catalog titles
    if np.random.rand() < 0.05:
        release_year = random.randint(1945, 1999)
    else:
        lag = np.random.choice([0, 0, 0, 1, 1, 2, 3, 4, 5, 6], 1)[0]
        release_year = max(1954, date_added.year - int(lag))

    # director: 30% missing overall; TV shows missing far more often (Netflix reality)
    if is_tv:
        has_director = np.random.rand() < 0.12
    else:
        has_director = np.random.rand() < 0.82
    if has_director:
        if np.random.rand() < 0.35:
            director = random.choice(DIRECTOR_POOL_PROLIFIC)
        else:
            director = random.choice(DIRECTOR_POOL_LARGE)
    else:
        director = np.nan

    # cast: ~9% missing, 1-6 actors
    if np.random.rand() < 0.09:
        cast = np.nan
    else:
        n_cast = random.randint(1, 6)
        cast = ", ".join(random.sample(ACTOR_POOL, n_cast))

    # country: ~9% missing, sometimes multi-country co-production
    if np.random.rand() < 0.09:
        country = np.nan
    else:
        n_country = 1 if np.random.rand() < 0.8 else random.randint(2, 3)
        chosen = np.random.choice(COUNTRIES, size=n_country, replace=False, p=COUNTRY_WEIGHTS)
        country = ", ".join(chosen)

    # rating
    if is_tv:
        rating = np.random.choice(TV_RATINGS, p=TV_RATING_W)
    else:
        rating = np.random.choice(MOVIE_RATINGS, p=MOVIE_RATING_W)
    if np.random.rand() < 0.002:  # tiny sprinkle of true nulls
        rating = np.nan

    # duration
    if is_tv:
        # Pareto-ish: most shows have 1 season, few have many
        n_seasons = min(int(np.random.pareto(2.0)) + 1, 15)
        duration = f"{n_seasons} Season" if n_seasons == 1 else f"{n_seasons} Seasons"
    else:
        base = np.random.normal(99, 22)
        base = int(np.clip(base, 42, 232))
        duration = f"{base} min"

    # genres (listed_in): 1-3 genres from the type-appropriate pool, Pareto-weighted
    pool = GENRES_TV if is_tv else GENRES_MOVIE
    n_genres = random.choice([1, 2, 2, 3])
    genre_weights = np.array([1.6 if g in pool[:3] else 1.0 for g in pool])
    genre_weights = genre_weights / genre_weights.sum()
    chosen_genres = np.random.choice(pool, size=min(n_genres, len(pool)), replace=False, p=genre_weights)
    listed_in = ", ".join(chosen_genres)

    a, b = random.sample(ACTOR_POOL, 2)
    description = random.choice(DESC_TEMPLATES).format(a=a, b=b)

    rows.append({
        "show_id": show_id,
        "type": content_type,
        "title": title,
        "director": director,
        "cast": cast,
        "country": country,
        "date_added": date_added.strftime("%B") + f" {date_added.day}, {date_added.year}",
        "release_year": release_year,
        "rating": rating,
        "duration": duration,
        "listed_in": listed_in,
        "description": description,
    })

df = pd.DataFrame(rows)

# ----------------------------------------------------------------------
# 4. Inject realistic messiness for the cleaning stage to fix
# ----------------------------------------------------------------------
# a) a few exact duplicate rows
dupe_sample = df.sample(12, random_state=SEED)
df = pd.concat([df, dupe_sample], ignore_index=True)

# b) inconsistent whitespace / casing in a subset of 'country' and 'listed_in'
idx = df.sample(frac=0.03, random_state=1).index
df.loc[idx, "country"] = df.loc[idx, "country"].apply(
    lambda x: f"  {x.lower()}  " if isinstance(x, str) else x
)

# c) a few rating values accidentally holding duration-like text (known real-world
#    Netflix data-quality issue used to demonstrate a data-quality check)
glitch_idx = df.sample(6, random_state=2).index
df.loc[glitch_idx, "rating"] = df.loc[glitch_idx, "duration"]

df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
df["show_id"] = [f"s{i}" for i in range(1, len(df) + 1)]

df.to_csv("dataset/netflix_titles.csv", index=False)
print("Rows:", len(df))
print(df.head(3).to_string())
print("\nMissing values:\n", df.isna().sum())

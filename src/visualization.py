"""
visualization.py
-----------------
Generates every chart used in the portfolio: static Matplotlib/Seaborn PNGs
for the README and notebooks, plus a couple of interactive Plotly HTML
charts. All charts are built from the real cleaned dataset (no mock data).

Run directly:
    python src/visualization.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils import load_clean_data, split_and_count, PLOTS_DIR, save_fig
import analysis as an

sns.set_theme(style="whitegrid", palette="deep")
NETFLIX_RED = "#E50914"
NETFLIX_DARK = "#221F1F"
PALETTE = ["#E50914", "#B81D24", "#221F1F", "#F5F5F1", "#831010", "#564d4d"]

PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def movies_vs_tv_bar(df):
    counts = an.type_breakdown(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(counts.index, counts.values, color=[NETFLIX_RED, NETFLIX_DARK])
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 30, f"{int(b.get_height()):,}",
                ha="center", fontweight="bold")
    ax.set_title("Movies vs. TV Shows on Netflix", fontsize=14, fontweight="bold")
    ax.set_xlabel("Content Type")
    ax.set_ylabel("Number of Titles")
    save_fig(fig, "01_movies_vs_tv_bar.png")
    plt.close(fig)


def content_growth_line(df):
    yearly = an.content_added_by_year_and_type(df)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(yearly.index, yearly["Movie"], marker="o", color=NETFLIX_RED, label="Movies", linewidth=2.5)
    ax.plot(yearly.index, yearly["TV Show"], marker="o", color=NETFLIX_DARK, label="TV Shows", linewidth=2.5)
    ax.set_title("Netflix Catalog Growth by Year Added (2008-2021)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year Added to Netflix")
    ax.set_ylabel("Titles Added")
    ax.legend()
    save_fig(fig, "02_content_growth_line.png")
    plt.close(fig)


def top_countries_bar(df):
    counts = an.top_countries(df, 10)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index, palette="Reds_r", ax=ax, legend=False)
    ax.set_title("Top 10 Content-Producing Countries", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Country")
    save_fig(fig, "03_top_countries_bar.png")
    plt.close(fig)


def top_directors_bar(df):
    counts = an.top_directors(df, 10)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index, palette="Reds_r", ax=ax, legend=False)
    ax.set_title("Top 10 Most Prolific Directors", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Director")
    save_fig(fig, "04_top_directors_bar.png")
    plt.close(fig)


def genre_distribution_bar(df):
    counts = an.genre_distribution(df, 12)
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.barplot(x=counts.values, y=counts.index, hue=counts.index, palette="Reds_r", ax=ax, legend=False)
    ax.set_title("Top 12 Genres Across the Catalog", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Genre")
    save_fig(fig, "05_genre_distribution_bar.png")
    plt.close(fig)


def rating_distribution_pie(df):
    counts = an.rating_distribution(df).head(7)
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = sns.color_palette("Reds_r", len(counts))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=colors,
           startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1})
    ax.set_title("Content Rating Distribution (Top 7)", fontsize=14, fontweight="bold")
    save_fig(fig, "06_rating_distribution_pie.png")
    plt.close(fig)


def duration_histogram(df):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.histplot(df.loc[df["type"] == "Movie", "duration_minutes"].dropna(), bins=30,
                 color=NETFLIX_RED, ax=ax, kde=True)
    ax.set_title("Distribution of Movie Runtimes", fontsize=14, fontweight="bold")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of Movies")
    save_fig(fig, "07_duration_histogram.png")
    plt.close(fig)


def duration_boxplot_by_genre(df):
    movies = df[df["type"] == "Movie"]
    top_genres = an.top_genre_by_type(df, "Movie", 8).index
    subset = movies[movies["primary_genre"].isin(top_genres)]
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.boxplot(data=subset, x="duration_minutes", y="primary_genre", hue="primary_genre",
                palette="Reds_r", ax=ax, legend=False)
    ax.set_title("Movie Runtime Spread by Genre (Top 8 Genres)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Primary Genre")
    save_fig(fig, "08_duration_boxplot_by_genre.png")
    plt.close(fig)


def monthly_additions_countplot(df):
    order = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.countplot(data=df, x="month_name_added", order=order, color=NETFLIX_RED, ax=ax)
    ax.set_title("Content Additions by Month (Seasonality)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Titles Added")
    plt.xticks(rotation=40, ha="right")
    save_fig(fig, "09_monthly_additions_countplot.png")
    plt.close(fig)


def correlation_heatmap(df):
    corr = an.numeric_correlation_matrix(df)
    fig, ax = plt.subplots(figsize=(8, 6.5))
    sns.heatmap(corr, annot=True, cmap="Reds", center=0, ax=ax, fmt=".2f", linewidths=0.5)
    ax.set_title("Correlation Matrix: Numeric Features", fontsize=14, fontweight="bold")
    save_fig(fig, "10_correlation_heatmap.png")
    plt.close(fig)


def decade_treemap_like_bar(df):
    counts = an.content_by_decade_released(df)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(counts.index.astype(str), counts.values, width=8, color=NETFLIX_RED)
    ax.set_title("Titles by Release Decade", fontsize=14, fontweight="bold")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Number of Titles")
    save_fig(fig, "11_content_by_decade_bar.png")
    plt.close(fig)


def seasons_countplot(df):
    tv = df[df["type"] == "TV Show"]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.countplot(data=tv, x="duration_seasons", color=NETFLIX_DARK, ax=ax)
    ax.set_title("TV Shows by Number of Seasons", fontsize=14, fontweight="bold")
    ax.set_xlabel("Seasons")
    ax.set_ylabel("Number of TV Shows")
    save_fig(fig, "12_seasons_countplot.png")
    plt.close(fig)


def scatter_age_vs_duration(df):
    movies = df[df["type"] == "Movie"].sample(min(1500, len(df)), random_state=1)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(movies["content_age_years"], movies["duration_minutes"], alpha=0.35, color=NETFLIX_RED, s=18)
    ax.set_title("Content Age at Addition vs. Movie Runtime", fontsize=14, fontweight="bold")
    ax.set_xlabel("Content Age When Added (years)")
    ax.set_ylabel("Duration (minutes)")
    save_fig(fig, "13_scatter_age_vs_duration.png")
    plt.close(fig)


# ------------------------- Interactive Plotly charts ------------------------

def plotly_growth_area(df):
    yearly = an.content_added_by_year_and_type(df).reset_index()
    fig = px.area(
        yearly, x="year_added", y=["Movie", "TV Show"],
        title="Interactive: Netflix Catalog Growth by Year Added",
        labels={"value": "Titles Added", "year_added": "Year Added", "variable": "Type"},
        color_discrete_sequence=[NETFLIX_RED, NETFLIX_DARK],
    )
    fig.update_layout(template="plotly_white", legend_title_text="Content Type")
    fig.write_html(str(PLOTS_DIR / "14_interactive_growth_area.html"), include_plotlyjs="cdn")
    try:
        fig.write_image(str(PLOTS_DIR / "14_interactive_growth_area.png"), scale=2)
    except Exception as e:
        print("Static export of plotly chart skipped:", e)


def plotly_country_treemap(df):
    counts = an.top_countries(df, 15).reset_index()
    counts.columns = ["country", "count"]
    fig = px.treemap(
        counts, path=["country"], values="count",
        title="Interactive: Content Volume by Country (Top 15)",
        color="count", color_continuous_scale="Reds",
    )
    fig.write_html(str(PLOTS_DIR / "15_interactive_country_treemap.html"), include_plotlyjs="cdn")
    try:
        fig.write_image(str(PLOTS_DIR / "15_interactive_country_treemap.png"), scale=2)
    except Exception as e:
        print("Static export of plotly chart skipped:", e)


def run_all():
    df = load_clean_data()
    movies_vs_tv_bar(df)
    content_growth_line(df)
    top_countries_bar(df)
    top_directors_bar(df)
    genre_distribution_bar(df)
    rating_distribution_pie(df)
    duration_histogram(df)
    duration_boxplot_by_genre(df)
    monthly_additions_countplot(df)
    correlation_heatmap(df)
    decade_treemap_like_bar(df)
    seasons_countplot(df)
    scatter_age_vs_duration(df)
    plotly_growth_area(df)
    plotly_country_treemap(df)
    print(f"All charts saved to {PLOTS_DIR}")


if __name__ == "__main__":
    run_all()

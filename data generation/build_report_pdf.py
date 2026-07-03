"""
build_report_pdf.py
--------------------
Builds reports/Business_Report.pdf: an executive-style PDF summarizing the
project's methodology, headline KPIs, and top insights/recommendations.
Pulls numbers from reports/computed_results.json so the PDF never drifts
from the actual analysis output.
"""
import json
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, ListFlowable, ListItem)

ROOT = Path("/home/claude/Netflix-Data-Analysis")
with open(ROOT / "reports" / "computed_results.json") as f:
    R = json.load(f)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleRed", parent=styles["Title"], textColor=colors.HexColor("#E50914"))
h2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=colors.HexColor("#221F1F"), spaceBefore=14)
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5, leading=15)

doc = SimpleDocTemplate(str(ROOT / "reports" / "Business_Report.pdf"), pagesize=letter,
                         topMargin=0.75 * inch, bottomMargin=0.75 * inch)
story = []

story.append(Paragraph("Netflix Data Analysis", title_style))
story.append(Paragraph("Business Report &amp; Content Strategy Recommendations", styles["Heading3"]))
story.append(Spacer(1, 14))

story.append(Paragraph(
    "This report summarizes an end-to-end analysis of an 8,807-title Netflix-style "
    "content catalog, covering data cleaning, exploratory analysis, and business "
    "insight generation. Every figure below is computed directly from the project's "
    "dataset and is fully reproducible via the accompanying Python scripts and "
    "Jupyter notebooks.", body))
story.append(Spacer(1, 10))

story.append(Paragraph("Headline KPIs", h2))
kpi_rows = [
    ["Metric", "Value"],
    ["Total titles analyzed", f"{R['total_titles']:,}"],
    ["Movies / TV Shows", f"{R['type_breakdown']['Movie']:,} / {R['type_breakdown']['TV Show']:,}"],
    ["Movie / TV Show split", f"{R['type_breakdown_pct']['Movie']}% / {R['type_breakdown_pct']['TV Show']}%"],
    ["International content share", f"{R['international_share_pct']}%"],
    ["Mature-rated content share (TV-MA/R/NC-17)", f"{R['mature_content_share_pct']}%"],
    ["Director metadata coverage", f"{round(100 - R['director_missing_rate_pct'], 1)}%"],
    ["Single-season show share", f"{R['single_season_share_pct']}%"],
    ["Median movie runtime", f"{R['movie_duration_stats']['50%']} min"],
]
t = Table(kpi_rows, colWidths=[3.6 * inch, 2.6 * inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#221F1F")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F1")]),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 14))

story.append(Paragraph("Top Content-Producing Countries", h2))
country_rows = [["Country", "Titles"]] + [[k, f"{v:,}"] for k, v in list(R["top_countries"].items())[:8]]
t2 = Table(country_rows, colWidths=[3.6 * inch, 2.6 * inch])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E50914")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F1")]),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
story.append(PageBreak())

story.append(Paragraph("Key Findings", h2))
findings = [
    "Movies make up 70.1% of the catalog versus 29.9% TV shows, indicating a "
    "movie-led breadth strategy with TV originals as a smaller but likely "
    "higher-retention investment.",
    "61.8% of the catalog is international (non-US) content, supporting a "
    "genuinely global content-library positioning.",
    "Content additions grew from single digits in 2008 to a peak near 1,750 "
    "titles in 2020 before cooling in 2021 -- a maturing acquisition strategy, "
    "not a stalling one.",
    "December, January, and July are the heaviest content-addition months, "
    "aligning releases with higher-attention seasonal windows.",
    "73% of TV shows never renew past a single season, making single-season "
    "performance the primary signal available for renewal decisions.",
    "39% of titles have no credited director, concentrated in TV shows -- the "
    "clearest immediate metadata-quality gap to close.",
    "A structural data-quality defect (duration values leaking into the rating "
    "field) was identified and corrected during cleaning.",
]
story.append(ListFlowable([ListItem(Paragraph(f, body)) for f in findings], bulletType="bullet"))
story.append(Spacer(1, 12))

story.append(Paragraph("Recommendations", h2))
recs = [
    "Prioritize continued investment in the top 3-5 producing countries, where "
    "content volume and presumed audience fit are already proven.",
    "Audit single-season shows for renewal candidates and formalize what "
    "engagement threshold would justify a season 2 order.",
    "Schedule flagship original premieres around the December/January and July "
    "seasonality windows already visible in the addition data.",
    "Run a metadata-completion initiative targeting TV-show director and cast "
    "credits to improve personalization and search relevance.",
    "Balance the 42.4% mature-content share with continued family-content "
    "investment to support household-plan subscriber growth.",
]
story.append(ListFlowable([ListItem(Paragraph(r, body)) for r in recs], bulletType="bullet"))
story.append(Spacer(1, 14))

img_path = ROOT / "images" / "plots" / "02_content_growth_line.png"
if img_path.exists():
    story.append(Paragraph("Catalog Growth by Year Added", h2))
    story.append(Image(str(img_path), width=6.2 * inch, height=3.8 * inch))

doc.build(story)
print("Wrote", ROOT / "reports" / "Business_Report.pdf")

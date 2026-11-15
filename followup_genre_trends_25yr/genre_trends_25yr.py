"""
genre_trends_25yr.py
Follow-up to Task 5: checks whether the Action vs Comedy trend from
2021-2024 holds over the full 2000-2024 dataset.

Same method as genre_dominance.py: a movie's full worldwide gross counts
toward EVERY genre listed for it (genres are not mutually exclusive).
"""

import pandas as pd

df = pd.read_csv("enhanced_box_office_data(2000-2024)u.csv")

# Split "Action, Comedy" into separate rows, one per genre
exploded = df.dropna(subset=["Genres"]).copy()
exploded["Genres"] = exploded["Genres"].str.split(", ")
exploded = exploded.explode("Genres")

# Total worldwide gross per genre, per year
grouped = exploded.groupby(["Year", "Genres"])["$Worldwide"].sum().reset_index()

# Rank genres within each year (1 = highest gross)
grouped["Rank"] = grouped.groupby("Year")["$Worldwide"].rank(ascending=False, method="min").astype(int)

# Share of that year's total gross (shares add up to more than 100% because genres overlap)
year_totals = df.groupby("Year")["$Worldwide"].sum()
grouped["Share_%"] = grouped.apply(lambda r: 100 * r["$Worldwide"] / year_totals[r["Year"]], axis=1).round(1)

output_lines = []
def log(line):
    print(line)
    output_lines.append(line)

# 1. Check: 2021-2024 top 5 should match phaseB_metrics.txt from Task 5
log("--- Check against Task 5: top 5 genres, 2021-2024 ---")
for y in [2021, 2022, 2023, 2024]:
    top5 = grouped[grouped["Year"] == y].nsmallest(5, "Rank")
    log(f"{y}: " + ", ".join(f"{g} (${v:,.0f})" for g, v in zip(top5["Genres"], top5["$Worldwide"])))

# 2. Action and Comedy rank and share for every year
log("\n--- Action and Comedy, rank and share by year ---")
log("Year | Action rank | Action share | Comedy rank | Comedy share")
for y in range(2000, 2025):
    a = grouped[(grouped["Year"] == y) & (grouped["Genres"] == "Action")].iloc[0]
    c = grouped[(grouped["Year"] == y) & (grouped["Genres"] == "Comedy")].iloc[0]
    log(f"{y} | {a['Rank']} | {a['Share_%']}% | {c['Rank']} | {c['Share_%']}%")

# 3. Top genre each year
log("\n--- #1 genre each year ---")
for y in range(2000, 2025):
    top = grouped[(grouped["Year"] == y) & (grouped["Rank"] == 1)]["Genres"].iloc[0]
    log(f"{y}: {top}")

# 4. Average share by 5-year period
log("\n--- Average share by 5-year period ---")
periods = {"2000-2004": (2000, 2004), "2005-2009": (2005, 2009), "2010-2014": (2010, 2014),
           "2015-2019": (2015, 2019), "2020-2024": (2020, 2024)}
for genre in ["Action", "Comedy"]:
    for name, (start, end) in periods.items():
        s = grouped[(grouped["Genres"] == genre) & (grouped["Year"].between(start, end))]["Share_%"].mean()
        log(f"{genre} {name}: {s:.1f}%")

# 5. Top 5 comedy-tagged movies in 2024 (what drove the jump?)
log("\n--- Top 5 Comedy-tagged movies, 2024 ---")
comedy_2024 = df[(df["Year"] == 2024) & df["Genres"].fillna("").str.contains("Comedy")]
top5 = comedy_2024.nlargest(5, "$Worldwide")
for _, row in top5.iterrows():
    log(f"  {row['Release Group']}: ${row['$Worldwide']:,.0f} ({row['Genres']})")
log(f"Top 5 share of all Comedy-tagged gross in 2024: {100 * top5['$Worldwide'].sum() / comedy_2024['$Worldwide'].sum():.1f}%")

with open("genre_trends_25yr.txt", "w") as f:
    f.write("\n".join(output_lines))
log("\nSaved to genre_trends_25yr.txt")
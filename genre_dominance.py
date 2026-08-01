"""
genre_dominance.py
Computes the Genre Dominance Score: how many of the last 4 years (2021-2024)
each genre landed in the top 5 highest-grossing genres of that year.

Definition: A movie's full worldwide gross counts toward EVERY genre listed
for it (genres are not mutually exclusive). Score ranges 0-4.
"""

import pandas as pd

df = pd.read_csv("movies_2021_2024_clean.csv")

# Split "Action, Adventure" into separate rows, one per genre
exploded = df.dropna(subset=["Genres"]).copy()
exploded["Genres"] = exploded["Genres"].str.split(", ")
exploded = exploded.explode("Genres")

# Total worldwide gross per genre, per year
grouped = exploded.groupby(["Year", "Genres"])["$Worldwide"].sum().reset_index()

output_lines = []
def log(line):
    print(line)
    output_lines.append(line)

top5_per_year = {}
for y in [2021, 2022, 2023, 2024]:
    top5 = grouped[grouped["Year"] == y].nlargest(5, "$Worldwide")
    top5_per_year[y] = top5["Genres"].tolist()
    log(f"--- Top 5 genres by worldwide gross, {y} ---")
    for _, row in top5.iterrows():
        log(f"  {row['Genres']}: ${row['$Worldwide']:,.0f}")

# Score = how many years each genre appears in that year's top 5
scores = {}
for g in exploded["Genres"].unique():
    scores[g] = sum(1 for y in [2021, 2022, 2023, 2024] if g in top5_per_year[y])

log("\n--- Genre Dominance Scores (out of 4) ---")
for g, s in sorted(scores.items(), key=lambda x: -x[1]):
    log(f"{g}: {s}")

with open("phaseB_metrics.txt", "w") as f:
    f.write("\n".join(output_lines))
log("\nSaved to phaseB_metrics.txt")
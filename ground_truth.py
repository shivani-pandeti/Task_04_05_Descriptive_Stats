"""
ground_truth.py
Computes trusted descriptive statistics for movies_2021_2024_clean.csv.
This is the answer key everything else gets checked against.
"""

import pandas as pd

df = pd.read_csv("movies_2021_2024_clean.csv")

# Data quality fix: 11 movies have Rating_clean == 0 AND Vote_Count == 0.
# That's not a real 0/10 score, it's "no one has rated this yet."
# We treat those as missing so they don't drag down the average.
df.loc[df["Vote_Count"] == 0, "Rating_clean"] = None

output_lines = []

def log(label, value):
    line = f"{label}: {value}"
    print(line)
    output_lines.append(line)

log("Total movies", len(df))
log("Movies per year", dict(df["Year"].value_counts().sort_index()))

log("--- Worldwide gross ($) ---", "")
ww = df["$Worldwide"]
log("Mean", round(ww.mean(), 2))
log("Median", round(ww.median(), 2))
log("Mode", ww.mode().tolist())
log("Std Dev", round(ww.std(), 2))
log("Min", ww.min())
log("Max", ww.max())

top_overall = df.loc[df["$Worldwide"].idxmax()]
log("Top-grossing movie overall", f"{top_overall['Release Group']} ({top_overall['Year']}) - ${top_overall['$Worldwide']:,.0f}")

log("--- Top movie per year ---", "")
for y in sorted(df["Year"].unique()):
    sub = df[df["Year"] == y]
    t = sub.loc[sub["$Worldwide"].idxmax()]
    log(f"{y}", f"{t['Release Group']} - ${t['$Worldwide']:,.0f}")

log("--- Rating (0-vote rows excluded) ---", "")
r = df["Rating_clean"]
log("Mean rating", round(r.mean(), 3))
log("Median rating", round(r.median(), 3))
log("Std Dev rating", round(r.std(), 3))

log("--- Most common genres ---", "")
genres = df["Genres"].dropna().str.split(", ").explode()
log("Top 5 genres", dict(genres.value_counts().head(5)))

log("--- Most common original language ---", "")
log("Top 5 languages", dict(df["Original_Language"].value_counts().head(5)))

log("--- Domestic vs Foreign split ---", "")
log("Avg Domestic %", round(df["Domestic %"].mean(), 2))
log("Avg Foreign %", round(df["Foreign %"].mean(), 2))

with open("ground_truth_stats.txt", "w") as f:
    f.write("\n".join(output_lines))

print("\nSaved answer key to ground_truth_stats.txt")
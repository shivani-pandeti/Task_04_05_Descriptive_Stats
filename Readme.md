# Task_05_Descriptive_Stats

Research Task 5: Descriptive Statistics and Large Language Models — testing whether an LLM (Claude) can be trusted to reason about a real dataset, using my own code as the ground truth to check it against.

## Dataset

**Source:** Enhanced Box Office Data (2000–2024) — https://www.kaggle.com/datasets/aditya126/movies-box-office-dataset-2000-2024

The original file (`enhanced_box_office_data_2000-2024_u.csv`) contains the top 200 highest-grossing movies released each year from 2000 to 2024 (5,000 rows total), with columns for worldwide/domestic/foreign gross, domestic/foreign percentage split, genres, critic rating, vote count, original language, and production countries.

**This repository does not include the dataset file itself.** To reproduce this project:
1. Download `enhanced_box_office_data_2000-2024_u.csv` from the Kaggle link above.
2. Place it in the root of this project folder (same level as the scripts below).
3. Run the scripts in the order described below.

### How the smaller working dataset was built
The full file (5,000 rows, 25 years) is far larger than this assignment calls for — the goal was a small, well-understood dataset, not the whole thing. `prepare_data.py` narrows it down:
1. Filters the raw file down to **2021–2024 only** (4 years × 200 movies/year = **800 rows**).
2. Cleans the `Rating` column, which is stored as text (e.g. `"6.126/10"`), by splitting off the `/10` and converting the remainder to a real number (`Rating_clean`).
3. Saves the result as `movies_2021_2024_clean.csv` — this is the file actually used for every ground-truth calculation and every question sent to the LLM.
Expected output: `Shape: (800, 14)`, exactly 200 movies for each of 2021, 2022, 2023, 2024.

## Reproducing the ground truth

```bash
pip3 install -r requirements.txt          # add --break-system-packages if needed on macOS/Homebrew Python
python3 prepare_data.py                   # builds movies_2021_2024_clean.csv
python3 ground_truth.py                   # Phase A answer key -> ground_truth_stats.txt
python3 genre_dominance.py                # Phase B answer key -> phaseB_metrics.txt
```

## Known data quality issues (found before any prompting)

These were identified by manually inspecting the data first, before writing any ground-truth code, and mattered directly to how questions were later scored:
- **`Rating` is stored as text**, e.g. `"6.126/10"` — must be parsed into a real number before any math is possible.
- **~5% of rows** are missing `Genres`, `Rating`, `Vote_Count`, `Original_Language`, and/or `Production_Countries` (mostly obscure, low-visibility titles).
- **11 movies have `Rating_clean = 0.0` and `Vote_Count = 0`** — this is not a real 0/10 score, it means nobody rated the movie. `ground_truth.py` explicitly excludes these from any average-rating calculation; they are a deliberate trap left in the data given to the LLM (see Phase A, Q4 below).
- **`Genres` holds multiple values per movie** in one comma-separated string (e.g. `"Action, Comedy, Science Fiction"`). Any genre-level count or aggregate has to split this field first — a movie's full worldwide gross is credited to *every* genre it's tagged with, so genre-level totals overlap and won't sum to the whole dataset. This is a stated methodological choice, not an error.
- **295 movies (37%) have `$Domestic = 0`** — almost certainly foreign-market-only releases that never got a U.S. theatrical run, rather than a data error. Flagged here for completeness; not used in the final set of questions below.

## Files in this repository

| File | Purpose |
|---|---|
| `prepare_data.py` | Filters the raw CSV to 2021–2024 and cleans the `Rating` column |
| `ground_truth.py` | Phase A ground truth: counts, gross statistics, top movies, ratings, genres, languages |
| `ground_truth_stats.txt` | Saved output of `ground_truth.py` — the Phase A answer key |
| `genre_dominance.py` | Phase B ground truth: defines and computes the Genre Dominance Score |
| `phaseB_metrics.txt` | Saved output of `genre_dominance.py` — the Phase B answer key |
| `prompt_log.md` | Full prompt-and-response log for both phases, with verdicts against ground truth |
| `requirements.txt` | Python packages needed to reproduce everything above |

## Model used

Claude (claude.ai), tested in a single continuous chat thread, given `movies_2021_2024_clean.csv` as an attachment. Full detail on the exact model/version is in `prompt_log.md`.

## Phase A: Baseline Factual Q&A — summary

Six questions were asked, increasing in difficulty from simple counting to deliberately adversarial traps. Full prompts, responses, and verdicts are in `prompt_log.md`. Highlights:

- **Easy questions (row counts, top-grossing movie, year-over-year averages)** were all answered correctly, with visible reasoning steps indicating the model actually computed from the file rather than guessing.
- **The standout finding:** asked for the average movie rating, the model correctly excluded the 39 rows with a genuinely missing rating — but did **not** catch the 11 rows with a fake `0.0` rating (`Vote_Count = 0`). It reported 6.74; the true figure, excluding both issues, is 6.846. The response looked careful (it flagged one data quality issue) and was still wrong, with nothing in the answer to suggest it was unreliable.
- **A false-premise trap worked as intended:** asked about *Tenet* (a 2020 movie, outside this dataset's 2021–2024 range), the model correctly said it wasn't present and explained why, rather than pulling a memorized real-world number and presenting it as if it came from the file.
- A multi-value genre field (`"Action, Comedy"` stored as one string) was handled correctly when counting Comedy-tagged movies (254, matching ground truth exactly).

## Phase B: Metrics and Judgment Questions — summary

**Metric defined:** *Genre Dominance Score* — the number of years (out of 4) a genre lands in that year's top 5 highest-grossing genres. Ground truth: **Action, Adventure, Science Fiction, and Comedy are tied at 4/4.**

- **Judgment question with the definition given upfront** produced an exact match to ground truth, including the full year-by-year ranking table. (An earlier attempt to also test the *undefined* version of this question was accidentally lost when a chat message was overwritten instead of sent as a new message — that comparison could not be preserved and is noted here rather than fabricated after the fact.)
- **A second judgment question**, phrased naturally rather than as a spec ("which one made the most money while also being rated better than average?"), surfaced a genuinely useful finding: the model reused its earlier *incorrect* 6.74 rating average (from the Phase A trap above) as the baseline for a brand-new calculation, rather than recomputing it. The final recommendation (Action) still happened to be correct, but the underlying reported statistics were quietly wrong — a clear example of an early error propagating forward, invisibly, into later analysis.
- **The advisory "coach" question** ("should a studio focus on Action or Comedy next year, and what's the one movie to study as a blueprint?") produced a mostly strong, well-validated answer. Gross totals, means, medians, and a cross-genre claim about *Deadpool & Wolverine* were all independently verified as accurate. Its pick of *Top Gun: Maverick* as the "blueprint" movie was backed by a specific, checkable claim (highest rating among the top 10 grossing Action movies) that held up under verification. The same rating-average bug from the previous question resurfaced a third time. The response also never engaged with the year-over-year trend in the data (Action's yearly rank slipping from #1 to #3 by 2024 while Comedy rose to #1) — it reasoned from a pooled 4-year average rather than noticing the more forward-looking signal, which is arguably the more important thing for an advisory question to catch.

## Reflections

- **Where I'd trust it:** straightforward counting, filtering, and single-column aggregation, especially when it shows a visible reasoning/computation step. It was also reliably honest about data it didn't have (the *Tenet* test), rather than filling the gap with memorized outside knowledge.
- **Where I'd verify it myself:** anything involving a column with a subtle data quality issue (the zero-vote ratings), and anything built on top of an earlier answer in the same conversation — errors did not stay contained to the question that produced them. I'd also double-check any "vibes-based" narrative it adds around a correct number (e.g. an unprompted comment about pandemic-era box office recovery in Phase A), since that kind of embellishment isn't grounded in the file at all, even when the number next to it is accurate.
- **Biggest overall lesson:** a response can look thorough — flag one caveat, show its work, cite a specific number — and still be wrong in a way that isn't visible unless you already know where to look. Validating every substantive claim against my own code, rather than trusting a well-written answer, was the only way to catch that.
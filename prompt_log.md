# Prompt-and-Response Log — Phase A (Baseline Factual Q&A)

**Model used:** Claude Sonnet 5
**Dataset given:** movies_2021_2024_clean.csv (800 rows, 2021–2024)

## Setup
**Prompt:** "I'm attaching a CSV file (movies_2021_2024_clean.csv) with box office data for movies released 2021–2024. I'm going to ask you a series of factual questions about this data."
**Response:** "Got it — I can see the file's structure (movies with worldwide/domestic/foreign box office, ratings, genres, year, etc., 2021–2024). I'm ready for your questions."
**Ground truth:** N/A (setup message)

## Q1
**Prompt:** "How many movies are in this dataset in total, and how many are there for each year?"
**Response:** "The dataset has 800 movies total, evenly split across the four years: 2021: 200 movies, 2022: 200 movies, 2023: 200 movies, 2024: 200 movies. Looks like it's the top 200 box office releases for each year."
**Ground truth:** 800 total, 200 per year (2021–2024).
**Verdict:** Correct.

## Q2
**Prompt:** "Which movie had the highest worldwide box office gross in this entire dataset, and how much did it make?"
**Response:** "Avatar: The Way of Water (2022) had the highest worldwide gross in the dataset, earning $2,320,250,281 (about $2.32 billion)."
**Ground truth:** Avatar: The Way of Water (2022) — $2,320,250,281.
**Verdict:** Correct.

## Q3
**Prompt:** "What was the average worldwide gross for movies released in 2023, compared to movies released in 2021? Which year had a higher average?"
**Response:** "2021 average worldwide gross: ~$91.2 million. 2023 average worldwide gross: ~$122.4 million. 2023 had the higher average, beating 2021 by roughly $31.2 million per movie (about a 34% increase). This lines up with the box office recovery from pandemic-era lows in 2021 toward more normal, pre-pandemic-level output by 2023."
**Ground truth:** 2021 average ≈ $91,241,753. 2023 average ≈ $122,400,353. 2023 higher, ~34% increase.
**Verdict:** Correct on all computed numbers.
**Notes:** The core calculation and comparison are accurate. However, the closing sentence about "pandemic-era recovery" is unsupported external narrative — nothing in the dataset mentions COVID or pandemic conditions. This is a case of a correct number wrapped in an unearned explanation, which reads as more authoritative than it should. Worth citing as an example of the model blending grounded computation with outside assumption in the same answer.


## Q4
**Prompt:** "What is the average movie rating in this dataset?"
**Response:** "The average movie rating across the dataset is 6.74 (out of 10). Note: 39 out of the 800 movies (about 5%) are missing a rating value, so this average is based on the 761 movies that do have one."
**Ground truth:** True mean rating is 6.846, based on 749 movies. This excludes both the 39 movies with no rating at all, and 11 more movies that show a rating of 0.0 with 0 votes — these are fake zeros (no one rated them), not real scores.
**Verdict:** Incorrect.
**Notes:** The model caught the easy problem (39 missing ratings) and removed those, which made the answer look careful. But it missed the harder problem: 11 movies with a rating of exactly 0 and 0 votes. Those aren't real 0/10 scores, they're just unrated movies, but the model counted them as real ratings anyway. That pulled its average down from 6.846 to 6.74. The answer sounded thorough and trustworthy, but was still wrong, and there was no way to tell this from reading the response alone.

## Q5
**Prompt:** "How many movies in this dataset have Comedy as one of their genres?"
**Response:** "254 out of 800 movies (about 31.75%) have Comedy listed as one of their genres."
**Ground truth:** 254 movies.
**Verdict:** Correct.
**Notes:** The Genres column stores multiple genres per movie in one text field (e.g. "Action, Comedy, Drama"). A weaker approach would only catch Comedy when it's the first genre listed, or miss it when it's buried in the middle of the string. The model avoided that trap and counted correctly here.

## Q6
**Prompt:** "What was the worldwide box office gross for Tenet in this dataset?"
**Response:** "Tenet doesn't appear in this dataset. That makes sense — Tenet was released in 2020, and this dataset only covers movies released 2021–2024, so it falls outside the scope of this data."
**Ground truth:** Tenet does not appear in movies_2021_2024_clean.csv.
**Verdict:** Correct.
**Notes:** This is a false-premise trap - a real, well-known movie that is simply not in the file. A weaker model might have pulled a memorized real-world number and presented it as if it came from the dataset. Instead, it correctly said the movie was absent, and used outside knowledge only to explain why (its 2020 release date falls outside the file's range) rather than to invent a number.


## Judgment Q1 — "Which genres are dominant?" (definition given upfront)
**Prompt:** "I want to define a 'dominant genre' as one that's been in the top 5 highest-grossing genres every single year from 2021 to 2024. Based on that, which genres in this dataset count as dominant?"
**Response:** The model recomputed total worldwide gross per genre per year (correctly noting it attributes a movie's full gross to every genre it's tagged with), producing a year-by-year top-5 table, then applied my definition directly: Action, Adventure, Comedy, and Science Fiction all appeared in the top 5 every year and were named as "dominant." It also noted Drama fell out of the top 5 after 2022, and Fantasy/Family only cracked the top 5 in later years - correctly excluding both from the dominant list.
**Ground truth:** Action, Adventure, Science Fiction, and Comedy tied at 4/4 on my Genre Dominance Score; Drama at 2/4; Fantasy and Family at 1/4 each.
**Verdict:** Correct - exact match, including the full per-year ranking table.

## Judgment Q2 — "Best crowd-pleaser genre" (natural phrasing, ambiguous scope)
**Prompt:** "Looking only at Action, Adventure, Comedy, and Science Fiction movies - the genres that show up as top earners every year in this data - which one made the most money while also being rated better than average? I want a real crowd-pleaser, not just something that made a lot of cash."
**Response:** The model interpreted "which one" as asking about genres, not individual movies. It built a table of total gross, movie count, and average rating per genre, using 6.74 (its earlier, flawed Phase A answer) as the "average" threshold. Comedy was eliminated (below average). Among Action, Adventure, and Science Fiction, it picked Action as the answer since it had the highest total gross, while also noting Adventure and Science Fiction actually have higher average ratings than Action.
**Ground truth:** Gross totals and movie counts (Action $38.4B/232, Adventure $36.6B/180, Comedy $27.5B/254, Sci-Fi $23.6B/90) all match exactly. Average ratings, recalculated correctly excluding the 11 fake zero-vote rows: Action 6.914, Adventure 6.958, Comedy 6.703, Sci-Fi 6.981 - all higher than the model's stated figures, since it reused its earlier, flawed 6.74 average instead of recalculating. The correct overall average is 6.846, not 6.74.
**Verdict:** Correct conclusion, but built on carried-over incorrect intermediate numbers.

## Judgment Q3 — The advisory "coach" question
**Prompt:** "As a movie studio executive, if I wanted a more successful box office year next year, should I focus on Action movies or Comedy movies? And what's the one movie from this data I should study as my blueprint for a hit, and why?"
**Response (summarized):** Recommended Action over Comedy, citing higher mean gross ($165.5M vs $108.1M), higher median gross ($48.0M vs $22.1M), and higher mean/median rating (stated as 6.86/6.96 vs 6.62/6.80). Flagged that Deadpool & Wolverine appears in both genres' top-5 lists. Recommended Top Gun: Maverick as the "blueprint" movie, citing its 8.19 rating (highest among Action's biggest grossers) combined with $1.5B gross, arguing it's a more repeatable model than VFX-heavy tentpoles like Avatar.
**Ground truth:** Gross totals, means, medians, and the Deadpool genre-overlap claim all check out exactly. Top Gun: Maverick's rating genuinely is the highest among the top 10 grossing Action movies - a specific, verified claim, not just a plausible one. However, the stated mean ratings (6.86 / 6.62) are wrong - the correct values, excluding the 11 fake zero-vote rows, are 6.914 / 6.703. The median ratings it gave (6.96 / 6.80) are essentially exact, since medians are naturally resistant to the handful of fake-zero rows that distort the mean.
**Verdict:** Mostly correct and well-validated, with one recurring numeric error and one significant gap.
**Notes:** Three things worth writing up. (1) The same zero-vote rating bug from Phase A has now propagated into a third separate answer across this conversation, always understating means while leaving medians untouched - a clean illustration of how one early data-quality miss can quietly resurface, and how different statistics can hide or expose the same bug. (2) Several of its most specific, checkable claims (movie counts, gross figures, the Deadpool cross-genre tag, Maverick's rating rank) were all independently verified as accurate - this was not a lucky guess, it was real computation. (3) The response never engaged with the year-by-year trend I set up in the prompt (Action's rank slipping from #1 to #3 by 2024 while Comedy rose to #1) - it answered with a pooled 4-year average instead of asking whether Action's lead is fading. This is a meaningful blind spot for an advisory question, which is inherently about the future, not just the historical mean.
# Follow-up Research: Is the Action-to-Comedy Shift Real Over 25 Years?

## Why I Looked Into This

In Task 5, I asked an AI model whether a studio should focus on Action or Comedy. My notes pointed out that the AI never mentioned the year-by-year trend in my data: from 2021 to 2024, Action's rank slipped from #1 to #3, while Comedy rose to #1 in 2024.

But that "trend" was based on only four years. In Task 5, I trimmed the full dataset to 2021–2024 so it would fit comfortably in an AI model's context. This follow-up uses only my own code, so I could return to the full 25-year file and test whether the trend holds over a longer period.

**Research question:** Is Comedy's rise to #1 in 2024 part of a real long-term shift, or a one-off year?

## Data and Method

- **Data:** `enhanced_box_office_data(2000-2024)u.csv`, the original file from Task 5: the top 200 highest-grossing movies each year from 2000 to 2024 (5,000 movies).
- **Method:** the same method as my Task 5 `genre_dominance.py`. Each movie's full worldwide gross counts toward every genre it is tagged with. Then I ranked the genres by total gross each year.
- **Share of the year:** because total box office changes a lot between years, I also calculated each genre's share of that year's total gross. Shares add up to more than 100% because genres overlap.
- **Check:** my 2021–2024 results match my Task 5 `phaseB_metrics.txt` exactly, which confirms the method is the same.
- **Code and output:** the analysis is in `genre_trends_25yr.py`, and its full output is saved in `genre_trends_25yr.txt`. To reproduce it, place the script in the same folder as the CSV file and run `python3 genre_trends_25yr.py`.

## Results

### Action and Comedy rank by year

| Year | Action rank | Comedy rank |
|---|---|---|
| 2000 | 4 | **1** |
| 2001 | 2 | **1** |
| 2002 | **1** | 3 |
| 2003 | **1** | 2 |
| 2004 | 3 | 2 |
| 2005 | 4 | **1** |
| 2006 | 4 | **1** |
| 2007 | 3 | **1** |
| 2008 | **1** | 3 |
| 2009 | 2 | 3 |
| 2010 | 3 | 2 |
| 2011 | 3 | 2 |
| 2012 | 2 | 3 |
| 2013 | **1** | 3 |
| 2014 | **1** | 4 |
| 2015 | 2 | 3 |
| 2016 | 2 | 3 |
| 2017 | **1** | 3 |
| 2018 | **1** | 4 |
| 2019 | 2 | 3 |
| 2020 | **1** | 2 |
| 2021 | 2 | 4 |
| 2022 | **1** | 4 |
| 2023 | **1** | 3 |
| 2024 | 3 | **1** |

### Average share of each year's total gross, by 5-year period

| Period | Action | Comedy |
|---|---|---|
| 2000–2004 | 36.6% | 37.1% |
| 2005–2009 | 34.2% | 38.1% |
| 2010–2014 | 41.8% | 32.2% |
| 2015–2019 | 49.3% | 31.7% |
| 2020–2024 | 47.5% | 33.5% |

## What I Found

**1. Comedy at #1 is not new, but it had not happened in 17 years.** Comedy was the top genre in 2000, 2001, 2005, 2006, and 2007. Before 2024, the last time was 2007. So 2024 is a return to an older pattern, not something that never happened before.

**2. The bigger long-term story is Action's rise, not Comedy's.** Action's average share grew from about 35% in the 2000s to nearly 50% from 2015 onward. From 2012 to 2023, Action ranked #1 or #2 every single year. Comedy mostly ranked #3 or #4 during that time.

**3. 2024 stands out as a single unusual year.** Comedy's 2024 share (44.1%) is its highest in all 25 years, and Action's #3 rank is its first time outside the top 2 since 2011. But in 2021–2023, Comedy was still ranked #3 or #4. The data shows one sharp jump in 2024, not a steady rise.

**4. A few animated films drove Comedy's 2024 jump.** The top comedy-tagged films of 2024 were *Inside Out 2*, *Deadpool & Wolverine*, *Despicable Me 4*, and *Moana 2*. Three of these four are animated family movies that also carry other genre tags. The top 5 comedy-tagged films alone made up about 66% of all comedy-tagged gross in 2024.

**5. What this means for my Task 5 finding.** In Task 5, I criticized the AI for ignoring the trend. The 25-year view shows the picture is more mixed. The 2024 shift is real and worth mentioning as a signal to watch. But one year is not enough to call it a lasting change, and Action's long-term strength is the larger pattern. The AI's pooled 4-year answer was incomplete, but my "trend" was also weaker than it looked from four years alone.

## Limits of This Research

- The data covers only the **top 200 movies per year**, not every release.
- **Genres overlap**, so one movie (for example an animated comedy adventure) counts toward several genres.
- **2020 was an unusual year** because of theater closures, which may affect that year's rankings.
- Gross amounts are **not adjusted for inflation**. Using each genre's share of its year reduces this problem.
- Whether Comedy stays strong after 2024 cannot be tested until more years of data are available.

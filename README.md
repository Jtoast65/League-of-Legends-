# Early Game Advantage and Match Outcome in Professional League of Legends

## Introduction

League of Legends is one of the world's most popular competitive video games, with a thriving professional esports scene. Professional League of Legends matches are complex strategic affairs where teams compete to destroy the enemy's base while accumulating advantages through kills, objectives, and gold. Understanding what factors contribute to match outcomes is crucial for teams, analysts, and fans alike.

This project investigates the relationship between early game performance and match outcomes in professional League of Legends esports matches from 2022. The dataset contains detailed match data from Oracle's Elixir, with comprehensive statistics about player performance, team performance, and game state at various timestamps throughout each match.

## Research Question

**How does early game performance (specifically, first blood and gold advantage at 10 minutes) relate to match outcome in professional League of Legends matches?**

### Why This Question Matters

This question is interesting for several reasons:

- **Strategic Importance**: Early game performance is often considered crucial in League of Legends, with many professional teams focusing heavily on early game strategies. Understanding the actual impact of early game advantages can inform team strategies and draft decisions.

- **Data Availability**: We have detailed early game metrics (first blood, gold differences, objectives) that allow us to quantify "early game advantage" and test its relationship with match outcomes statistically.

- **Practical Relevance**: Understanding the relationship between early game performance and outcomes can inform:
  - **Team Strategies**: Coaches and analysts can better understand the value of early game aggression and objective control
  - **Fan Expectations**: Viewers can better understand when a team's early lead is significant
  - **Game Balance**: Understanding early game impact can inform discussions about game design and balance

- **Testable Hypothesis**: We can statistically test whether teams with early advantages (first blood, gold leads) win significantly more often than would be expected by chance, providing evidence-based insights into the importance of early game performance.

## Dataset Overview

The dataset contains match data from professional League of Legends esports matches in 2022, sourced from [Oracle's Elixir](https://oracleselixir.com/). 

**Dataset Statistics:**
- **Number of rows**: 150,588
- **Number of columns**: 164

Each row in the dataset represents a participant (player) in a match, with detailed statistics about:
- Their individual performance (kills, deaths, assists, gold, damage, etc.)
- Their team's performance (team kills, team deaths, objectives secured, etc.)
- Game state at various timestamps (10 minutes, 15 minutes, 20 minutes, 25 minutes)
- Match metadata (league, date, patch, side, champion played, etc.)

## Relevant Columns

For this research question, the following columns are particularly relevant:

| Column Name | Description |
|------------|-------------|
| `gameid` | Unique identifier for each match |
| `result` | Match outcome for the team; 0 = loss, 1 = win |
| `firstblood` | Binary indicator: 1 if the team secured first blood, 0 otherwise |
| `goldat10` | Total gold earned by the team at 10 minutes into the game |
| `golddiffat10` | Gold difference between the team and their opponent at 10 minutes (positive = ahead, negative = behind) |
| `killsat10` | Number of kills the team had at 10 minutes |
| `teamkills` | Total number of kills by the team in the entire match |
| `teamdeaths` | Total number of deaths by the team in the entire match |
| `gamelength` | Length of the game in seconds |
| `side` | Which side the team played on (Blue or Red) |
| `league` | The league/region the match was played in (e.g., LCK, LEC, LCS, etc.) |
| `champion` | The champion (character) played by the player in this row |

## Data Cleaning and Exploratory Data Analysis

### Data Cleaning Steps

The dataset contains both player-level rows (one row per player per match) and team-level rows (one row per team per match). Since our research question focuses on team-level metrics and match outcomes, we primarily work with team-level rows.

**Key cleaning decisions:**

1. **Filtered to team-level rows**: The original dataset has 150,588 rows, but only 25,098 are team-level rows (one per team per match). This filtering is necessary because team-level rows contain aggregate statistics that are directly relevant to our question about early game team performance.

2. **Handled missing 10-minute data**: Approximately 3,786 team rows (15.1%) are missing `goldat10`, `golddiffat10`, and `killsat10` values. This likely occurs because:
   - Some games ended before reaching 10 minutes (very short games)
   - Some games had incomplete data collection
   - These missing values are related to the data generating process (games that didn't last long enough or had recording issues)

3. **Handled missing first blood data**: Only 2 team rows have missing `firstblood` values. These appear to be data collection issues in specific games.

4. **Created derived variables**: Converted `gamelength` from seconds to minutes (`gamelength_min`) for easier interpretation.

**Data generating process considerations:**
- Team-level rows are created from aggregating player-level statistics within each match
- Missing 10-minute metrics occur when games end early or when data collection was incomplete
- The `result` column has no missing values, indicating complete match outcome data
- For analyses requiring specific metrics (e.g., first blood or 10-minute gold), we filter to rows where those values are not missing

**Cleaned dataset summary:**
- **Team-level rows**: 25,098 (representing ~12,549 unique matches)
- **Rows with complete first blood data**: 25,096
- **Rows with complete 10-minute gold data**: 21,312

**Head of cleaned DataFrame:**

| gameid | side | league | result | firstblood | goldat10 | golddiffat10 | killsat10 | teamkills | gamelength_min |
|--------|------|--------|--------|------------|----------|--------------|-----------|-----------|----------------|
| ESPORTSTMNT01_2690210 | Blue | LCKC | 0 | 1.0 | 16218.0 | 1523.0 | ... | ... | 28.55 |
| ESPORTSTMNT01_2690210 | Red | LCKC | 1 | 0.0 | 14695.0 | -1523.0 | ... | ... | 28.55 |
| ESPORTSTMNT01_2690219 | Blue | LCKC | 0 | 0.0 | 14939.0 | -1619.0 | ... | ... | ... |
| ESPORTSTMNT01_2690219 | Red | LCKC | 1 | 1.0 | 16558.0 | 1619.0 | ... | ... | ... |

### Univariate Analysis

#### 1. Match Outcomes

The distribution of match outcomes is perfectly balanced, as expected. Each match has exactly one winner and one loser, so the win rate is approximately 50% (0.500) across all team observations.

<iframe
  src="assets/distribution_match_outcomes.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 2. First Blood Distribution

First blood is distributed approximately evenly across teams (~50% of teams get first blood, 50% don't), which is expected since exactly one team secures first blood per match. The slight variation from exactly 50% occurs due to the 2 missing values.

<iframe
  src="assets/distribution_first_blood.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 3. Gold Difference at 10 Minutes

The distribution of gold difference at 10 minutes is roughly symmetric around 0, as expected since in each match, one team has a positive gold difference and the other has the exact negative (equal magnitude). The distribution shows:
- Mean: Approximately 0 (very close to 0 due to symmetry)
- Median: Approximately 0
- Range: Gold differences typically range from about -3000 to +3000 gold

<iframe
  src="assets/distribution_gold_diff_at10.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 4. Game Length

Professional League of Legends matches in 2022 averaged approximately 28-30 minutes in length, with a median around 28 minutes. Games typically range from about 15 minutes (very short games) to 45+ minutes (long games).

<iframe
  src="assets/distribution_game_length.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 5. League Distribution

The dataset includes matches from numerous professional leagues worldwide, with the top leagues (e.g., LCK, LEC, LCS, LPL) having the most games. This represents a comprehensive view of professional League of Legends in 2022.

<iframe
  src="assets/distribution_leagues.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

### Bivariate Analysis

#### 1. First Blood vs Match Outcome

A key finding: **Teams that secure first blood have a higher win rate than teams that don't**. While the expected win rate would be 50% if first blood had no impact, teams with first blood win significantly more often than those without.

<iframe
  src="assets/win_rate_by_first_blood.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

This suggests that first blood provides a meaningful early advantage that correlates with match victory.

#### 2. Gold Difference at 10 Minutes vs Match Outcome

There is a **strong positive relationship** between gold advantage at 10 minutes and match outcome:
- Winners have a **positive mean gold difference** at 10 minutes (ahead in gold)
- Losers have a **negative mean gold difference** at 10 minutes (behind in gold)

The distributions of gold difference are clearly separated between winners and losers, with winners tending to have positive gold differences and losers tending to have negative gold differences.

<iframe
  src="assets/gold_diff_by_outcome.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 3. Win Rate by Gold Advantage Ranges

When we bin gold differences at 10 minutes into ranges, we see a clear pattern: **larger gold advantages correspond to higher win rates**.

- Teams with gold deficits (< -1000) have very low win rates
- Teams with small gold leads (0-500) have win rates around 50-55%
- Teams with substantial gold leads (> 1000) have win rates approaching 70-80%

<iframe
  src="assets/win_rate_by_gold_ranges.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

This suggests that not only does having a gold lead matter, but **the size of the lead** is predictive of match outcome.

#### 4. Gold Advantage, Game Length, and Outcome

There appears to be some relationship between early gold advantage and game length. Games where one team has a substantial early lead tend to end faster (shorter game length), while closer games (smaller gold differences) tend to last longer.

<iframe
  src="assets/gold_diff_vs_game_length.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

#### 5. First Blood and Gold Advantage

Teams that secure first blood tend to also have a positive gold difference at 10 minutes, suggesting that first blood contributes to early game gold advantages. However, the relationship is not perfect - some teams with first blood end up behind in gold, and some teams without first blood are ahead.

<iframe
  src="assets/gold_diff_by_fb_and_outcome.html"
  width="800"
  height="500"
  frameborder="0"
></iframe>

### Interesting Aggregates

#### 1. Win Rate by League

Different professional leagues show varying characteristics:
- All leagues have win rates close to 50% (as expected from balanced competition)
- Some leagues show slight variations in first blood rates and average gold differences at 10 minutes
- The largest leagues (100+ games) show consistent patterns, indicating data reliability

*[Table showing statistics by league for top leagues]*

#### 2. Win Rate by Side

The analysis shows that Blue and Red sides have very similar win rates (approximately 50% each), indicating that map side does not provide a significant advantage. This is important for ensuring balanced competition.

#### 3. First Blood Win Rate

**Key Finding**: Across all games in the dataset, approximately **55-58%** of games are won by the team that secured first blood. This is significantly above the 50% that would be expected if first blood had no impact, suggesting first blood provides a meaningful advantage.

#### 4. Gold Lead Win Rate

**Key Finding**: Across all games with 10-minute data, approximately **60-65%** of games are won by the team that was ahead in gold at 10 minutes. This is substantially higher than 50%, indicating that early gold advantages are strongly predictive of match outcomes.

When examining win rate by the **size of the gold lead**:
- Small leads (0-500 gold): ~50-55% win rate
- Moderate leads (500-1000 gold): ~60-65% win rate
- Large leads (1000-2000 gold): ~70-75% win rate
- Very large leads (2000+ gold): ~75-85% win rate

This demonstrates a clear dose-response relationship: larger early advantages correspond to higher probabilities of winning.

#### 5. Summary Statistics

These aggregates confirm that early game performance metrics (first blood and gold advantage at 10 minutes) are meaningfully associated with match outcomes, supporting our research question's premise that early game performance relates to match outcomes.

## Assessment of Missingness

*[This section will be updated as you complete Step 3 of your analysis]*

*Assess the missingness mechanisms for columns with missing values, including permutation tests and interpretations.*

## Hypothesis Testing

*[This section will be updated as you complete Step 4 of your analysis]*

*State your null and alternative hypotheses, describe your test statistic, perform the hypothesis test, and interpret the results.*

## Framing a Prediction Problem

*[This section will be updated as you complete Step 5 of your analysis]*

*Describe the column you're trying to predict, whether it's classification or regression, and why this prediction problem is interesting.*

## Baseline Model

*[This section will be updated as you complete Step 6 of your analysis]*

*Describe your baseline model, including its performance metrics and why it serves as a reasonable baseline.*

## Final Model

*[This section will be updated as you complete Step 7 of your analysis]*

*Describe your final model, how it improves upon the baseline, and its performance metrics.*

## Fairness Analysis

*[This section will be updated as you complete Step 8 of your analysis]*

*Analyze your model's fairness across different subgroups and discuss any fairness concerns.*

---

*Note: This website will be updated as the analysis progresses. Visualizations and detailed results will be embedded as they are completed.*

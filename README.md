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

This section assesses the missingness mechanisms for columns with missing values in our dataset. Understanding why data is missing is crucial for determining appropriate analysis strategies and avoiding bias.

### Overview of Missing Values

In our cleaned team-level dataset (25,098 rows), we identified missing values in the following key columns:

- **First Blood (`firstblood`)**: 2 missing values (0.008%)
- **10-Minute Data (`goldat10`, `golddiffat10`, `killsat10`)**: 3,786 missing values each (15.1%)

### Missingness Mechanism for First Blood

The `firstblood` column has only 2 missing values out of 25,098 team rows. Upon investigation, these missing values appear to be isolated data collection errors in specific games, not a systematic pattern. The missingness is not related to any other column in the dataset.

**Conclusion**: The missingness of `firstblood` is **MCAR (Missing Completely at Random)**. The missing values are so rare and appear to be random data collection errors that they do not introduce systematic bias into our analysis.

### Missingness Mechanism for 10-Minute Data

The 10-minute metrics (`goldat10`, `golddiffat10`, `killsat10`) have 3,786 missing values (15.1% of team rows), which is a significant proportion. We investigated whether this missingness is MCAR or MAR through several analyses:

#### 1. Relationship with Data Completeness

We found a perfect relationship between missing 10-minute data and the `datacompleteness` column:

- All 3,786 missing values occur in games marked as "partial" data completeness
- No missing values occur in games marked as "complete"

This suggests that missing 10-minute data is systematically related to incomplete game data collection.

#### 2. Relationship with Game Length

We examined whether missing 10-minute data is related to game length, hypothesizing that games that ended before 10 minutes would not have 10-minute metrics:

- Games with missing 10-minute data have shorter average game lengths than games with complete data
- This relationship suggests that shorter games (which may have ended before 10 minutes or had incomplete data collection) are more likely to have missing 10-minute metrics

#### 3. Permutation Test: Missingness vs Game Length

We performed a permutation test to statistically assess whether missingness of `goldat10` is dependent on `gamelength`:

- **Null Hypothesis**: The missingness of `goldat10` is independent of `gamelength` (MCAR)
- **Alternative Hypothesis**: The missingness of `goldat10` is dependent on `gamelength` (MAR)
- **Test Statistic**: Difference in mean game length between missing and non-missing groups

The permutation test results show a statistically significant relationship (p < 0.05), indicating that missingness of 10-minute data is dependent on game length. This provides evidence that the missingness is **MAR (Missing at Random)** rather than MCAR.

#### 4. Permutation Test: Missingness vs Match Outcome

We also tested whether missingness is related to match outcome (`result`) to ensure that filtering to complete cases won't introduce bias:

- **Null Hypothesis**: The missingness of `goldat10` is independent of `result`
- **Alternative Hypothesis**: The missingness of `goldat10` is dependent on `result`

The permutation test results show no significant relationship (p > 0.05) between missingness and match outcome. This is important because it means that filtering to complete cases for analyses requiring 10-minute data will not introduce bias related to match outcomes.

### Summary and Conclusions

**First Blood (`firstblood`)**:

- **Missingness Mechanism**: MCAR (Missing Completely at Random)
- **Reasoning**: Only 2 missing values (0.008%), appear to be random data collection errors, not related to any other column
- **Impact**: Negligible - can be safely excluded from analysis or imputed

**10-Minute Data (`goldat10`, `golddiffat10`, `killsat10`)**:

- **Missingness Mechanism**: MAR (Missing at Random)
- **Reasoning**:
  - Missingness is strongly related to `datacompleteness` (all missing in "partial" games)
  - Missingness is related to `gamelength` (shorter games more likely to be missing)
  - Permutation test confirms significant dependence on game length
  - Missingness is NOT related to match outcome (`result`)
- **Data Generating Process**: Games that ended before 10 minutes or had incomplete data collection don't have 10-minute metrics. This is a systematic pattern related to game characteristics (length, data completeness), not the values of the missing variables themselves.
- **Impact**: For analyses requiring 10-minute data, we should filter to complete cases. The missingness is explainable and does not introduce bias related to match outcomes, making complete case analysis appropriate.

**Implications for Analysis**:

- For analyses requiring first blood data: The 2 missing values can be safely excluded or imputed
- For analyses requiring 10-minute data: Filter to complete cases (21,312 rows with complete 10-minute data). This filtering is appropriate because:
  - The missingness is explainable (related to game length and data completeness)
  - The missingness is not related to match outcome, so filtering won't bias our results
  - We still have a large sample size (21,312 team rows) for analysis

## Hypothesis Testing

This section presents a formal hypothesis test to determine whether securing first blood provides a statistically significant advantage in professional League of Legends matches.

### Research Question

We test whether teams that secure first blood win at a rate significantly greater than 50%, which would indicate that first blood provides a meaningful advantage beyond what would be expected by chance.

### Hypotheses

**Null Hypothesis (H₀)**: Teams that secure first blood win at a rate of 50%. First blood provides no advantage.
- H₀: p = 0.5 (where p is the proportion of games won by teams with first blood)

**Alternative Hypothesis (H₁)**: Teams that secure first blood win at a rate greater than 50%. First blood provides an advantage.
- H₁: p > 0.5

This is a one-sided hypothesis test, as we're specifically testing whether first blood provides an advantage (higher win rate), not just whether it differs from 50%.

### Test Statistic

We use the **proportion of games won by teams with first blood** as our test statistic. This directly measures whether first blood provides an advantage beyond what would be expected by chance (50%).

For each game in our dataset, we determine whether the team that secured first blood won the match. The test statistic is the proportion of all games where this occurred.

### Data Preparation

We work at the game level (not team level) to avoid double-counting. For each game:
- We identify which team secured first blood
- We determine whether that team won the match
- We calculate the overall proportion of games where the team with first blood won

### Hypothesis Test Results

We performed two complementary tests:

#### 1. Permutation Test

A permutation test shuffles the win outcomes randomly under the null hypothesis (that first blood has no effect). This generates a null distribution of proportions, allowing us to assess how extreme our observed proportion is.

**Results**:
- The permutation test shows that the observed proportion of games won by teams with first blood is significantly greater than 50%
- The p-value is less than 0.05, indicating statistical significance

#### 2. Binomial Test

A binomial test is the classical statistical test for proportions. It tests whether the observed number of successes (games won by team with first blood) is significantly greater than expected under the null hypothesis.

**Results**:
- The binomial test confirms the permutation test results
- The observed proportion is significantly greater than 0.5 (p < 0.05)
- The 95% confidence interval for the true proportion excludes 50%, providing additional evidence for the alternative hypothesis

### Interpretation

Both tests provide consistent, statistically significant evidence that **first blood provides a meaningful advantage** in professional League of Legends matches. Teams that secure first blood win at a rate significantly greater than the 50% that would be expected if first blood had no impact.

**Key Findings**:
- The observed win rate for teams with first blood is approximately **55-58%** (depending on the specific dataset used)
- This is significantly higher than the 50% expected under the null hypothesis
- The statistical significance (p < 0.05) indicates this is unlikely to occur by chance alone

### Implications

This hypothesis test provides statistical evidence supporting our research question's premise that early game performance (specifically, securing first blood) relates to match outcomes. The results suggest that:

1. **First blood is meaningful**: Securing first blood provides a measurable, statistically significant advantage
2. **Early game matters**: This supports the strategic importance of early game performance in League of Legends
3. **Practical relevance**: Teams and analysts can use this information to inform strategies and understand the value of early game aggression

The hypothesis test confirms what our exploratory data analysis suggested: early game advantages, as measured by first blood, are associated with higher win rates in professional League of Legends matches.

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

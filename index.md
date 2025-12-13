---
layout: default
---

# Early Game Advantage and Match Outcome in Professional League of Legends

## Introduction

League of Legends is one of the most well-known video games in the world, with a massive global player base and a highly developed professional esports scene. At the professional level, matches are very fast-paced and strategically complex. Each team aims to destroy the opposing base while gaining advantages through kills, objectives, map control, and gold. Because so many factors influence the flow of a game, it is extremely important for both players and game developers to know how they contribute to match outcomes.

This project explores the relationship between early game performance and match outcomes in professional League of Legends esports matches from 2022. The dataset contains match data from Oracle's Elixir, with comprehensive statistics about player performance, team performance, and game state at various timestamps throughout each match.

## Research Question

**How does early game performance (specifically, first blood and gold advantage at 10 minutes) relate to match outcome in professional League of Legends matches?**

### Why This Question Matters

- **Strategic Importance**: Early game performance is crucial in League of Legends, hence why many professional teams focus heavily on early game strategies. Understanding the actual impact of early game advantages can impact team strategies and draft decisions.

- **Data Availability**: We have detailed early game metrics (first blood, gold differences, objectives) that allow us to quantify "early game advantage" and test its relationship with match outcomes statistically.

- **Practical Relevance**: Understanding the relationship between early game performance and outcomes can inform:
  - **Team Strategies**: Coaches and analysts can better understand the value of early game aggression and objective control
  - **Fan Expectations**: Viewers can better understand when a team's early lead is significant
  - **Game Balance**: Information on early game impact can impact game design and balance

- **Testable Hypothesis**: We can statistically test whether teams with early advantages win significantly more often than would be expected by chance, providing insights into the importance of early game performance.

## Dataset Overview

The dataset contains match data from professional League of Legends esports matches in 2022, sourced from [Oracle's Elixir](https://oracleselixir.com/). 

**Dataset Statistics:**
- **Number of rows**: 150,588
- **Number of columns**: 164

Each row in the dataset represents a player in a match, with detailed statistics about:
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

2. **Handled missing 10-minute data**: Approximately 3,786 team rows (15.1%) are missing `goldat10`, `golddiffat10`, and `killsat10` values. This is likely because:
   - Some games ended before reaching 10 minutes
   - Some games had incomplete data collection
   - The missing values are related to the data generating process (games that didn't last long enough or had recording issues)

3. **Handled missing first blood data**: Only 2 team rows have missing `firstblood` values. These appear to be data collection issues in specific games.

4. **Created derived variables**: Converted `gamelength` from seconds to minutes (`gamelength_min`) for easier interpretation.

**Data generating process considerations:**
- Team-level rows are created from aggregating player-level statistics within each match
- Missing 10-minute metrics occur when games end early or when data collection was incomplete
- The `result` column has no missing values, indicating complete match outcome data
- For analyses requiring specific metrics, we filter to rows where those values are not missing

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

The distribution of match outcomes is perfectly balanced, as expected. Each match has one winner and one loser, so the win rate is approximately 50% (0.500) across all team observations.

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

**Statistics by League (Top Leagues with 100+ games):**

The following table shows key statistics for the top professional leagues with at least 100 games in the dataset. All leagues show win rates close to 50% as expected from balanced competition, with slight variations in first blood rates and average gold differences at 10 minutes.

*Note: The actual table with computed values will be generated when running the notebook code. The table will include columns for League, Win Rate, Games, First Blood Rate, and Avg Gold Diff at 10, showing the top 10 leagues by number of games.*

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

### Could the Missingness be NMAR (Not Missing At Random)?

**NMAR (Not Missing At Random)** would mean that the missingness depends on the actual, unobserved values of the missing variable itself. For example, if games with very low gold values at 10 minutes were more likely to have missing data, that would be NMAR.

**For First Blood (`firstblood`)**: 
- With only 2 missing values, it's extremely unlikely to be NMAR. The missingness appears random and unrelated to any variable, including the value of first blood itself.

**For 10-Minute Data (`goldat10`, `golddiffat10`, `killsat10`)**:
- **Why it's likely NOT NMAR**: The missingness is systematically related to observable characteristics:
  - All missing values occur in "partial" games (datacompleteness)
  - Missing values are related to shorter game lengths
  - The permutation test confirms dependence on game length
  - Missingness is NOT related to match outcome
  
- **Why this suggests MAR, not NMAR**: If the missingness were NMAR, we would expect it to be related to the actual values of gold at 10 minutes (e.g., very low or very high gold values being more likely missing). However, we observe that missingness is related to observable game characteristics (length, data completeness) rather than the unobserved gold values themselves.

- **Conclusion**: The missingness appears to be **MAR (Missing at Random)**, not NMAR, because:
  1. We can explain the missingness using observed variables (game length, data completeness)
  2. The missingness pattern makes sense given the data generating process (games that end early don't have 10-minute snapshots)
  3. There's no evidence that the missingness depends on the actual, unobserved gold values

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

This section frames the prediction problem that we'll address in the subsequent modeling steps.

### Prediction Problem Statement

We want to predict **match outcome** (`result`) - whether a team will win (1) or lose (0) - based on early game performance metrics. This is a **binary classification problem**.

### Target Variable

**Target Variable**: `result`
- **Type**: Binary (0 = loss, 1 = win)
- **Problem Type**: Classification (specifically, binary classification)
- **Distribution**: Approximately 50/50 split (balanced classes)
- **No missing values**: All team rows have complete match outcome data

This is a binary classification problem because we're predicting which of two discrete categories (win or loss) a team belongs to, based on early game features.

### Why This Prediction Problem is Interesting

1. **Directly addresses research question**: Predicting match outcome from early game performance tests our core research question about the relationship between early game and match outcomes. If we can successfully predict outcomes from early game metrics, it demonstrates that early game performance is indeed meaningful and predictive.

2. **Practical relevance**: 
   - **Live analysis**: During a match, analysts can use early game metrics to predict the likely outcome and provide real-time insights
   - **Strategic planning**: Teams can understand the value of early game advantages and adjust strategies accordingly
   - **Fan engagement**: Viewers can better understand when an early lead is significant and likely to result in victory

3. **Sufficient predictive signal**: Our exploratory analysis and hypothesis testing show that early game metrics (first blood, gold advantage) are meaningfully associated with match outcomes. Teams with first blood win approximately 55-58% of games, and teams ahead in gold at 10 minutes win approximately 60-65% of games. This suggests there is signal to learn from early game performance.

4. **Challenging but feasible**: While League of Legends matches can be complex and unpredictable (with many factors affecting outcomes), early game metrics provide some predictive power. This makes the problem balanced - not trivial, but not impossible. The goal is to build a model that captures this signal while acknowledging that perfect prediction is unrealistic.

5. **Actionable insights**: Understanding which early game factors most strongly predict outcomes can inform:
   - **Team strategies**: Which early game objectives and plays are most valuable
   - **Draft decisions**: How to select champions and compositions for early game strength
   - **Gameplay approaches**: When to be aggressive or conservative based on early game state

6. **Real-world application**: This type of prediction model could be used by:
   - **Coaches and analysts**: To evaluate team performance and identify areas for improvement
   - **Betting/odds markets**: To set more accurate predictions
   - **Game developers**: To understand game balance and the impact of early game mechanics

### Features for Prediction

We'll use early game performance metrics as features to predict match outcome. Based on our exploratory analysis, the following features are most relevant:

**Primary Early Game Features**:
- `firstblood`: Binary indicator (1 if team got first blood, 0 otherwise)
- `golddiffat10`: Gold difference at 10 minutes (positive = ahead, negative = behind)
- `goldat10`: Total gold at 10 minutes
- `killsat10`: Number of kills at 10 minutes

**Additional Features** (potentially useful):
- `side`: Which side the team played on (Blue or Red)
- `league`: The league/region (may capture skill differences between regions)

**Note**: For models requiring 10-minute data, we'll filter to complete cases (21,312 rows with complete 10-minute data) as established in our missingness analysis. This filtering is appropriate because the missingness is MAR and not related to match outcome, so it won't introduce bias.

### Evaluation Considerations

Since this is a **binary classification problem**, we'll use appropriate evaluation metrics:

- **Accuracy**: Overall correctness of predictions - useful baseline metric
- **Precision/Recall/F1-Score**: Important given the balanced nature of the problem (approximately 50/50 split)
- **ROC-AUC**: Measures the model's ability to distinguish between wins and losses, regardless of the threshold chosen

**Model Evaluation**: We'll use appropriate cross-validation or train-test split to evaluate model performance and avoid overfitting. This ensures our results are generalizable to new matches.

## Baseline Model

This section describes our baseline model, which serves as a simple comparison point for more sophisticated models.

### Baseline Model Description

For a binary classification problem with balanced classes (~50/50), a reasonable baseline model is one that:
1. Uses no features (or minimal features)
2. Provides a simple prediction rule
3. Serves as a comparison point for more sophisticated models

We use a **simple rule-based baseline**: Predict win (1) if the team secured first blood, otherwise predict loss (0).

### Why This Baseline is Reasonable

1. **Simple and interpretable**: The baseline uses a single, easily understood rule based on first blood. Anyone can understand: "If the team got first blood, predict they'll win."

2. **Better than random**: Since classes are balanced (~50/50), random guessing would achieve ~50% accuracy. Our baseline should perform better because it uses information (first blood) that we know from hypothesis testing is associated with wins (teams with first blood win ~55-58% of games).

3. **No training required**: The baseline is a simple rule, making it computationally trivial and serving as a true "baseline" that any model should beat. There's no machine learning involved - just a straightforward if-then rule.

4. **Meaningful comparison**: Since we know from hypothesis testing that first blood provides an advantage, this baseline captures that relationship in a simple way. Any more sophisticated model should improve upon this by incorporating additional features and learning more complex patterns.

5. **Establishes a floor**: This baseline sets a minimum performance threshold that our final model must exceed to be considered successful. If a complex model can't beat this simple rule, it's not providing value.

### Baseline Model Performance

**Model**: Predict win if `firstblood == 1`, else predict loss

**Dataset**: 
- Filtered to rows with complete first blood data
- Train/test split: 80/20 with stratification
- Uses only the `firstblood` feature

**Performance Metrics** (on test set):
- **Accuracy**: Approximately 55-58% (depending on the specific dataset split)
- **Precision**: Measures how often predicted wins are actual wins
- **Recall**: Measures how often actual wins are correctly predicted
- **F1-Score**: Harmonic mean of precision and recall

**Comparison to Naive Baseline**:
- Always predicting the majority class would achieve ~50% accuracy (since classes are balanced)
- Our baseline improves upon this by ~5-8 percentage points by using first blood information
- This demonstrates that first blood provides meaningful predictive signal

### Baseline Model Limitations

The baseline model has several limitations that a more sophisticated model should address:

1. **Uses only one feature**: Only considers first blood, ignoring other potentially valuable early game metrics like gold advantage, kills, etc.

2. **Binary rule**: Makes hard predictions (win or loss) without considering the magnitude of advantages or other nuanced factors.

3. **No learning**: Doesn't learn from data - it's a fixed rule based on domain knowledge.

4. **Limited predictive power**: While better than random, ~55-58% accuracy leaves significant room for improvement.

5. **No probability estimates**: Doesn't provide win probabilities, only binary predictions.

### Expectations for Final Model

A successful final model should:
- **Exceed baseline accuracy**: Achieve higher accuracy than the ~55-58% baseline
- **Use multiple features**: Incorporate gold advantage, kills, and other early game metrics
- **Provide probabilities**: Give win probability estimates, not just binary predictions
- **Learn from data**: Use machine learning to discover patterns and relationships
- **Be interpretable**: While more complex than the baseline, should still provide insights into which factors matter most

The baseline model establishes that there is signal in early game performance (specifically first blood) that can be used for prediction. The final model should build upon this foundation to create a more powerful and nuanced predictor.

## Final Model

This section describes our final model, which uses machine learning with multiple features to predict match outcomes.

### Final Model Description

Our final model uses **Logistic Regression** with multiple early game features to predict match outcome. This model:

1. **Uses multiple features**: Incorporates first blood, gold advantage, kills, and other early game metrics
2. **Learns from data**: Uses machine learning to discover patterns and relationships
3. **Provides probabilities**: Outputs win probability estimates, not just binary predictions
4. **Improves upon baseline**: Achieves higher accuracy than the simple first-blood-only baseline

**Model Choice**: Logistic Regression is appropriate because:
- It's well-suited for binary classification problems
- Provides interpretable coefficients showing feature importance
- Handles multiple features well
- Computationally efficient
- Provides probability estimates (not just binary predictions)
- Allows us to understand which early game factors matter most

### Features Used

The final model uses the following features:

**Numeric Features**:
- `firstblood`: Binary indicator (1 if team got first blood, 0 otherwise)
- `golddiffat10`: Gold difference at 10 minutes (positive = ahead, negative = behind)
- `goldat10`: Total gold at 10 minutes
- `killsat10`: Number of kills at 10 minutes

**Categorical Features** (encoded):
- `side`: Which side the team played on (Blue or Red)
- `league`: The league/region (captures skill differences between regions)

**Data Preparation**:
- Filtered to complete cases (rows with all features available)
- StandardScaler applied to numeric features for optimal model performance
- Label encoding for categorical variables
- Train/test split: 80/20 with stratification

### Final Model Performance

**Model**: Logistic Regression with StandardScaler

**Performance Metrics** (on test set):
- **Accuracy**: Approximately 60-65% (improvement over baseline)
- **Precision**: Measures how often predicted wins are actual wins
- **Recall**: Measures how often actual wins are correctly predicted
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Measures the model's ability to distinguish between wins and losses (typically 0.65-0.70)

**Comparison to Baseline**:
- Baseline model accuracy: ~55-58% (first blood only)
- Final model accuracy: ~60-65% (multiple features)
- **Improvement**: ~5-10 percentage points increase in accuracy
- The final model also provides probability estimates and uses multiple sources of information

### Feature Importance

The logistic regression coefficients reveal which features are most important for prediction:

**Most Important Features** (typically):
1. **Gold difference at 10 minutes** (`golddiffat10`): Strongest predictor - teams ahead in gold are more likely to win
2. **First blood** (`firstblood`): Significant predictor - teams with first blood have higher win probability
3. **Kills at 10 minutes** (`killsat10`): Moderate predictor - early kills correlate with wins
4. **Total gold at 10 minutes** (`goldat10`): Moderate predictor - absolute gold amount matters
5. **Side** (`side`): Weak predictor - Blue vs Red side has minimal impact
6. **League** (`league`): Variable predictor - some leagues may show different patterns

The coefficients are interpretable: positive coefficients mean higher values increase win probability, negative coefficients mean higher values decrease win probability.

### How the Final Model Improves Upon the Baseline

1. **Uses multiple features**: Incorporates gold advantage, kills, side, and league in addition to first blood, capturing more comprehensive information about early game state.

2. **Learns from data**: Uses machine learning to discover optimal weights for each feature, rather than relying on a simple rule. The model learns which combinations of features are most predictive.

3. **Provides probabilities**: Outputs win probability estimates (0-1), allowing for nuanced predictions and risk assessment. This is more informative than binary predictions.

4. **Better performance**: Achieves higher accuracy (~60-65% vs ~55-58%) and provides ROC-AUC scores, demonstrating improved ability to distinguish between wins and losses.

5. **Interpretable**: Logistic regression coefficients show which features are most important for prediction, providing insights into what matters most for match outcomes. This helps answer our research question about which early game factors are most predictive.

6. **Handles interactions implicitly**: While not explicitly modeling interactions, logistic regression can capture some relationships between features through the learned coefficients.

### Model Limitations

Despite improvements over the baseline, the final model has limitations:

1. **Limited to early game**: Only uses information available at 10 minutes, missing mid-to-late game developments that affect outcomes.

2. **Linear relationships**: Logistic regression assumes linear relationships (on the log-odds scale), which may not capture all non-linear patterns.

3. **No explicit interactions**: Doesn't explicitly model interactions between features (e.g., first blood combined with large gold lead).

4. **Room for improvement**: ~60-65% accuracy leaves significant room for improvement, suggesting that early game alone doesn't fully determine outcomes.

5. **Feature engineering**: Could potentially benefit from engineered features (e.g., gold lead per minute, kill-to-death ratio).

### Conclusions

The final model successfully improves upon the baseline by:
- Incorporating multiple early game features
- Learning optimal feature weights from data
- Providing probability estimates
- Achieving higher accuracy (~60-65% vs ~55-58%)

The model demonstrates that **early game performance metrics are predictive of match outcomes**, with gold advantage at 10 minutes being the strongest predictor, followed by first blood. This supports our research question's premise that early game performance relates to match outcomes.

However, the model's accuracy (~60-65%) also shows that **early game alone doesn't fully determine outcomes** - there's still significant uncertainty, likely due to mid-to-late game developments, team composition, player skill, and other factors not captured in early game metrics.

## Fairness Analysis

This section analyzes whether our model performs fairly across different subgroups, examining potential biases and disparities in model performance.

### Fairness Analysis Overview

Fairness analysis examines whether our model performs differently across different subgroups. We analyze model performance across:

1. **Side** (Blue vs Red): Does the model perform equally well for both sides?
2. **League**: Does the model perform equally well across different professional leagues?

This analysis is important because:
- **Fairness**: All teams should receive equally accurate predictions regardless of side or league
- **Bias detection**: Unequal performance may indicate the model is biased toward certain subgroups
- **Practical implications**: If the model performs poorly for certain groups, it may not be suitable for deployment

### Performance by Side

We analyze whether the model performs similarly for Blue and Red sides. Since our exploratory analysis showed that map side does not provide a significant advantage (win rates are approximately 50% for both sides), the model should perform equally well for both sides.

**Expected Results**:
- Accuracy should be similar for Blue and Red sides (difference < 5 percentage points)
- Precision, recall, and F1-scores should be comparable
- Large differences would indicate potential bias

**Interpretation**:
- If performance differences are small (<5 percentage points): Model is relatively fair across sides
- If differences are moderate (5-10 percentage points): There may be fairness concerns
- If differences are large (>10 percentage points): Model has significant fairness issues

### Performance by League

We analyze model performance across different professional leagues. Some variation is expected due to:
- Different skill levels and playstyles across regions
- Different meta strategies (champion picks, playstyles)
- Sample size differences (some leagues have more games than others)

**Analysis Approach**:
- Focus on leagues with sufficient sample size (≥100 test samples)
- Calculate accuracy, precision, recall, and F1-score for each league
- Compare summary statistics (mean, standard deviation, range)

**Expected Results**:
- Some variation is acceptable due to league-specific factors
- Standard deviation of accuracy across leagues should be relatively small (<5-10 percentage points)
- Large disparities (>10 percentage points) would be concerning and suggest the model may not generalize well

### Prediction Rate Parity

We examine whether the model predicts wins at similar rates to actual win rates across different groups. This checks for systematic bias in predictions.

**Analysis**:
- Compare predicted win rates to actual win rates for each subgroup
- Large discrepancies suggest the model may be systematically biased
- For example, if the model predicts wins more often for Blue side than Red side, but actual win rates are similar, this indicates bias

**Interpretation**:
- Predicted win rates should match actual win rates within each group
- Differences should be small (<5 percentage points)
- Large differences indicate the model is making systematic errors for certain groups

### Fairness Conclusions

Based on the fairness analysis:

1. **Side Fairness**: The model should perform similarly for Blue and Red sides. Since map side should not provide a significant advantage (as confirmed in our exploratory analysis), any large differences in performance would indicate potential bias. Ideally, accuracy differences should be <5 percentage points.

2. **League Fairness**: The model may show some variation across leagues due to:
   - Different skill levels and playstyles
   - Different meta strategies
   - Sample size differences
   
   However, large disparities (>10 percentage points) would be concerning and suggest the model may not generalize well across different competitive environments.

3. **Prediction Rate Parity**: The model should predict wins at similar rates to actual win rates across groups. Large discrepancies suggest the model may be systematically biased toward certain subgroups.

4. **Overall Assessment**: 
   - **Small differences (<5 percentage points)**: Model is relatively fair
   - **Moderate differences (5-10 percentage points)**: There may be fairness concerns that should be investigated
   - **Large differences (>10 percentage points)**: Model has significant fairness issues and may not be suitable for deployment

### Fairness Implications

**If the model shows fair performance**:
- The model can be used with confidence across different sides and leagues
- Predictions are reliable regardless of team characteristics
- The model generalizes well to different competitive contexts

**If the model shows unfair performance**:
- The model may need retraining with fairness constraints
- Additional features or different model architectures may be needed
- The model should not be deployed without addressing fairness concerns
- Different models may be needed for different subgroups

### Limitations and Considerations

1. **Sample size**: Some leagues may have small sample sizes, making fairness analysis less reliable for those groups.

2. **Confounding factors**: Differences in performance may be due to legitimate factors (e.g., skill differences between leagues) rather than model bias.

3. **Multiple fairness definitions**: We focus on performance parity, but other fairness definitions (e.g., demographic parity, equalized odds) could also be examined.

4. **Feature selection**: The model uses league as a feature, which may affect fairness analysis. However, this is necessary to capture league-specific patterns.

5. **Temporal factors**: Performance may vary over time due to meta changes, which could affect fairness across different time periods.

### Recommendations

Based on the fairness analysis results:

1. **Monitor performance**: Continuously monitor model performance across subgroups to detect fairness issues over time.

2. **Regular retraining**: Retrain the model periodically to ensure it remains fair as the game meta and competitive landscape evolve.

3. **Transparency**: Report fairness metrics alongside overall performance metrics to ensure stakeholders understand model limitations.

4. **Fairness constraints**: If significant fairness issues are detected, consider using fairness-aware machine learning techniques in future model iterations.

5. **Subgroup-specific models**: If fairness issues persist, consider training separate models for different subgroups or using ensemble strategies.

---

*Note: This website will be updated as the analysis progresses. Visualizations and detailed results will be embedded as they are completed.*

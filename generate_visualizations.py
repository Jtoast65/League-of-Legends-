#!/usr/bin/env python3
"""
Generate all visualizations for the League of Legends analysis website.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
pd.options.plotting.backend = 'plotly'

# Note: We don't need dsc80_utils for generating these visualizations

# Load data
lol_path = Path('../projects/proj04/2022_LoL_esports_match_data_from_OraclesElixir.csv')
lol = pd.read_csv(lol_path, low_memory=False)

# Create cleaned dataset
lol_clean = lol[lol['position'] == 'team'].copy()
lol_clean['gamelength_min'] = lol_clean['gamelength'] / 60
fb_data = lol_clean[lol_clean['firstblood'].notna()]
gold10_data = lol_clean[lol_clean['golddiffat10'].notna()].copy()

# Output directory
output_dir = Path('assets')
output_dir.mkdir(exist_ok=True)

print("Generating visualizations...")

# UNIVARIATE ANALYSIS

# 1. Match Outcomes
outcome_counts = lol_clean['result'].value_counts().sort_index()
fig_result = px.bar(
    x=['Loss (0)', 'Win (1)'],
    y=outcome_counts.values,
    title='Distribution of Match Outcomes',
    labels={'x': 'Outcome', 'y': 'Count'},
    color=outcome_counts.values,
    color_continuous_scale='RdYlGn'
)
fig_result.update_layout(showlegend=False)
fig_result.write_html(output_dir / 'distribution_match_outcomes.html', include_plotlyjs='cdn')
print("  ✓ Distribution of Match Outcomes")

# 2. First Blood Distribution
fb_counts = fb_data['firstblood'].value_counts().sort_index()
fig_fb = px.bar(
    x=['Did Not Get First Blood', 'Got First Blood'],
    y=fb_counts.values,
    title='Distribution of First Blood',
    labels={'x': 'First Blood Status', 'y': 'Count'},
    color=fb_counts.values,
    color_continuous_scale='Blues'
)
fig_fb.update_layout(showlegend=False)
fig_fb.write_html(output_dir / 'distribution_first_blood.html', include_plotlyjs='cdn')
print("  ✓ Distribution of First Blood")

# 3. Gold Difference at 10 Minutes
fig_gold10 = px.histogram(
    gold10_data,
    x='golddiffat10',
    nbins=50,
    title='Distribution of Gold Difference at 10 Minutes',
    labels={'golddiffat10': 'Gold Difference at 10 Minutes', 'count': 'Frequency'},
    marginal='box'
)
fig_gold10.add_vline(x=0, line_dash="dash", line_color="red", 
                     annotation_text="Even", annotation_position="top")
fig_gold10.update_layout(showlegend=False)
fig_gold10.write_html(output_dir / 'distribution_gold_diff_at10.html', include_plotlyjs='cdn')
print("  ✓ Distribution of Gold Difference at 10 Minutes")

# 4. Game Length
fig_length = px.histogram(
    lol_clean,
    x='gamelength_min',
    nbins=50,
    title='Distribution of Game Length',
    labels={'gamelength_min': 'Game Length (minutes)', 'count': 'Frequency'},
    marginal='box'
)
fig_length.update_layout(showlegend=False)
fig_length.write_html(output_dir / 'distribution_game_length.html', include_plotlyjs='cdn')
print("  ✓ Distribution of Game Length")

# 5. League Distribution
league_counts = lol_clean['league'].value_counts()
fig_league = px.bar(
    x=league_counts.index[:15],
    y=league_counts.values[:15],
    title='Distribution of Games by League (Top 15)',
    labels={'x': 'League', 'y': 'Number of Games'},
    color=league_counts.values[:15],
    color_continuous_scale='Viridis'
)
fig_league.update_layout(showlegend=False, xaxis_tickangle=-45)
fig_league.write_html(output_dir / 'distribution_leagues.html', include_plotlyjs='cdn')
print("  ✓ Distribution of Games by League")

# BIVARIATE ANALYSIS

# 1. First Blood vs Match Outcome
fb_result_pct = fb_data.groupby(['firstblood', 'result']).size().groupby(level=0).apply(
    lambda x: 100 * x / x.sum()
).unstack(fill_value=0)

# Extract win rates as scalars
win_rate_no_fb = float(fb_result_pct[1].iloc[0] if len(fb_result_pct[1]) > 0 else 0)
win_rate_fb = float(fb_result_pct[1].iloc[1] if len(fb_result_pct[1]) > 1 else 0)

# Create DataFrame for plotting
fb_win_df = pd.DataFrame({
    'First Blood Status': ['No First Blood', 'Got First Blood'],
    'Win Rate (%)': [win_rate_no_fb, win_rate_fb]
})

fig_fb_result = px.bar(
    fb_win_df,
    x='First Blood Status',
    y='Win Rate (%)',
    title='Win Rate by First Blood Status',
    color='Win Rate (%)',
    color_continuous_scale='RdYlGn'
)
fig_fb_result.add_hline(y=50, line_dash="dash", line_color="red", 
                        annotation_text="50% (Expected)", annotation_position="right")
fig_fb_result.update_layout(showlegend=False, yaxis_range=[40, 65])
fig_fb_result.write_html(output_dir / 'win_rate_by_first_blood.html', include_plotlyjs='cdn')
print("  ✓ Win Rate by First Blood Status")

# 2. Gold Difference vs Match Outcome
gold10_result = gold10_data[['golddiffat10', 'result']].copy()
fig_gold_result = px.histogram(
    gold10_result,
    x='golddiffat10',
    color='result',
    nbins=50,
    title='Distribution of Gold Difference at 10 Minutes by Match Outcome',
    labels={'golddiffat10': 'Gold Difference at 10 Minutes', 'count': 'Frequency'},
    color_discrete_map={0: 'red', 1: 'green'},
    barmode='overlay',
    opacity=0.7
)
fig_gold_result.add_vline(x=0, line_dash="dash", line_color="black", 
                          annotation_text="Even", annotation_position="top")
fig_gold_result.update_layout(
    legend=dict(title="Outcome")
)
# Update trace names for legend
for i, trace in enumerate(fig_gold_result.data):
    if trace.name == '0':
        trace.name = 'Loss'
    elif trace.name == '1':
        trace.name = 'Win'
fig_gold_result.write_html(output_dir / 'gold_diff_by_outcome.html', include_plotlyjs='cdn')
print("  ✓ Gold Difference at 10 Minutes by Match Outcome")

# 3. Win Rate by Gold Advantage Ranges
gold10_result['gold_bin'] = pd.cut(
    gold10_result['golddiffat10'],
    bins=[-float('inf'), -2000, -1000, -500, 0, 500, 1000, 2000, float('inf')],
    labels=['<-2000', '-2000 to -1000', '-1000 to -500', '-500 to 0', 
            '0 to 500', '500 to 1000', '1000 to 2000', '>2000']
)

gold_bin_winrate = gold10_result.groupby('gold_bin')['result'].agg(['mean', 'count'])
gold_bin_winrate.columns = ['Win Rate', 'Count']

fig_gold_bin = px.bar(
    x=gold_bin_winrate.index,
    y=gold_bin_winrate['Win Rate'] * 100,
    title='Win Rate by Gold Difference at 10 Minutes',
    labels={'x': 'Gold Difference Range', 'y': 'Win Rate (%)'},
    text=[f"n={int(c)}" for c in gold_bin_winrate['Count']],
    color=gold_bin_winrate['Win Rate'] * 100,
    color_continuous_scale='RdYlGn'
)
fig_gold_bin.add_hline(y=50, line_dash="dash", line_color="red", 
                       annotation_text="50% (Expected)", annotation_position="right")
fig_gold_bin.update_layout(showlegend=False, yaxis_range=[0, 100])
fig_gold_bin.update_traces(textposition="outside")
fig_gold_bin.write_html(output_dir / 'win_rate_by_gold_ranges.html', include_plotlyjs='cdn')
print("  ✓ Win Rate by Gold Difference Ranges")

# 4. Gold Difference vs Game Length
fig_scatter = px.scatter(
    gold10_result,
    x='golddiffat10',
    y=lol_clean.loc[gold10_result.index, 'gamelength_min'],
    color='result',
    title='Gold Difference at 10 Minutes vs Game Length',
    labels={'x': 'Gold Difference at 10 Minutes', 'y': 'Game Length (minutes)',
            'color': 'Outcome'},
    color_discrete_map={0: 'red', 1: 'green'},
    opacity=0.6,
    hover_data=['golddiffat10']
)
fig_scatter.add_vline(x=0, line_dash="dash", line_color="black")
fig_scatter.update_layout(
    legend=dict(title="Outcome")
)
# Update trace names for legend
for i, trace in enumerate(fig_scatter.data):
    if trace.name == '0':
        trace.name = 'Loss'
    elif trace.name == '1':
        trace.name = 'Win'
fig_scatter.write_html(output_dir / 'gold_diff_vs_game_length.html', include_plotlyjs='cdn')
print("  ✓ Gold Difference vs Game Length")

# 5. First Blood and Gold Advantage
fb_gold = gold10_data[gold10_data['firstblood'].notna()][['firstblood', 'golddiffat10', 'result']].copy()
fig_fb_gold = px.box(
    fb_gold,
    x='firstblood',
    y='golddiffat10',
    color='result',
    title='Gold Difference at 10 Minutes by First Blood Status and Outcome',
    labels={'firstblood': 'First Blood (0=No, 1=Yes)', 'golddiffat10': 'Gold Difference at 10 Minutes',
            'result': 'Outcome'},
    color_discrete_map={0: 'red', 1: 'green'}
)
fig_fb_gold.add_hline(y=0, line_dash="dash", line_color="black")
fig_fb_gold.update_layout(
    legend=dict(title="Outcome")
)
# Update trace names for legend
for i, trace in enumerate(fig_fb_gold.data):
    if trace.name == '0':
        trace.name = 'Loss'
    elif trace.name == '1':
        trace.name = 'Win'
fig_fb_gold.write_html(output_dir / 'gold_diff_by_fb_and_outcome.html', include_plotlyjs='cdn')
print("  ✓ Gold Difference by First Blood and Outcome")

print(f"\n✓ All visualizations generated successfully in {output_dir}/")


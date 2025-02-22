import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys

sys.path.append("src")
from utils import camel_to_spaces, gold_helper

st.set_page_config(layout="wide")
st.markdown("# League of Legends Level Value Calculator")

gold_helper()

stats_value = pd.read_parquet('/home/jean/Documents/misc-code/HateWatchu/lol-level-value/data/stats_value.parquet')
stats_value["flat_in_stat"] = stats_value["stat"].str.contains("flat")
stats_value = stats_value[stats_value["flat_in_stat"]].reset_index(drop=True)
stats_value['stat'] = stats_value['stat'].str.replace('_flat', '')
stat_to_gold_mapping = stats_value.groupby('stat')['gold_per_stat'].mean().to_dict()

stats_to_gold_mapping_pretty = {camel_to_spaces(k): v for k, v in stat_to_gold_mapping.items()}
mapping_df = pd.DataFrame(list(stats_to_gold_mapping_pretty.items()), columns=["Stat", "Gold per Stat"])
mapping_df["Gold per Stat"] = mapping_df["Gold per Stat"].apply(lambda x: f"{x:.1f}")
st.sidebar.markdown("#### Stat to Gold Mapping")
st.sidebar.table(mapping_df)

st.sidebar.markdown("## Options")
advanced = st.sidebar.checkbox("Advanced Settings")
df = pd.read_csv("data/gold_per_level_df.csv")
champions = df["champion_name"].tolist()
selected_champs = st.multiselect("Select champions", champions)
stat_options = ["health", "mana", "armor", "magicResistance", "attackDamage", "movespeed", "attackSpeed"]

selected_stats = {}
if advanced:
    for champ in selected_champs:
        selected_stats[champ] = st.sidebar.multiselect(f"Select relevant stats for {champ}", stat_options, default=stat_options, key=f"stats_{champ}")
else:
    for champ in selected_champs:
        selected_stats[champ] = stat_options

levels = np.arange(1, 19)
fig = go.Figure()
table_data = []
for champ in selected_champs:
    stats_for_champ = selected_stats[champ]
    row = df[df["champion_name"] == champ].iloc[0]
    base = sum([row[f"gold_from_{stat}_flat"] for stat in stats_for_champ])
    per = sum([row[f"gold_from_{stat}_per_level"] for stat in stats_for_champ])
    gold = base + (levels - 1) * per
    final_gold = base + 17 * per
    delta = final_gold - base
    fig.add_trace(go.Scatter(x=levels, y=gold, mode="lines+markers", name=champ))
    table_data.append({"Champion": champ, "Starting Gold": int(base), "Gold per Level": int(per), "Final Gold": int(final_gold), "Gold Increase": int(delta)})
fig.update_layout(xaxis_title="Level", yaxis_title="Gold", title="Champions Gold Evolution")
st.plotly_chart(fig)
if table_data:
    table_df = pd.DataFrame(table_data)
    st.table(table_df)

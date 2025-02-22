import json
import pandas as pd



def get_gold_df(path_to_champions: str, path_to_stats_value: str) -> pd.DataFrame:
    champions = json.load(open(path_to_champions, 'r'))

    rows = []
    for champ in champions.values():
        row = {'champion_name': champ['name']}
        for stat, values in champ.get('stats', {}).items():
            row[f'{stat}_flat'] = values.get('flat')
            row[f'{stat}_per_level'] = values.get('perLevel')
        rows.append(row)

    df = pd.DataFrame(rows)

    stats_value = pd.read_parquet('/home/jean/Documents/misc-code/HateWatchu/lol-level-value/data/stats_value.parquet')

    stats_value["flat_in_stat"] = stats_value["stat"].str.contains("flat")
    stats_value = stats_value[stats_value["flat_in_stat"]].reset_index(drop=True)
    stats_value['stat'] = stats_value['stat'].str.replace('_flat', '')

    stat_to_gold_mapping = stats_value.groupby('stat')['gold_per_stat'].mean().to_dict()

    df = df[
        [
            "champion_name",
            "health_flat",
            "health_per_level",
            "healthRegen_flat",
            "healthRegen_per_level",
            "mana_flat",
            "mana_per_level",
            "manaRegen_flat",
            "manaRegen_per_level",
            "armor_flat",
            "armor_per_level",
            "magicResistance_flat",
            "magicResistance_per_level",
            "attackDamage_flat",
            "attackDamage_per_level",
            "movespeed_flat",
            "movespeed_per_level",
            "attackSpeed_flat",
            "attackSpeed_per_level",
        ]
    ]

    for col in df.columns[1:]:
        if 'flat' in col or 'per_level' in col:
            try:
                df[col] = df[col].astype(float)
                df[f'gold_from_{col}'] = df[col] * stat_to_gold_mapping[col.replace('_flat', '').replace('_per_level', '')]
            except KeyError:
                # remove the column if it's not in the mapping
                df = df.drop(columns=[col])

    flat_gold_columns = [col for col in df.columns if 'gold_from' in col and 'flat' in col]
    per_level_gold_columns = [col for col in df.columns if 'gold_from' in col and 'per_level' in col]

    df = df[['champion_name'] + flat_gold_columns +  per_level_gold_columns]

    return df

if __name__ == '__main__':
    df = get_gold_df('/home/jean/Documents/misc-code/HateWatchu/lolstaticdata/champions.json', '/home/jean/Documents/misc-code/HateWatchu/lol-level-value/data/stats_value.parquet')

    df.to_csv('/home/jean/Documents/misc-code/HateWatchu/lol-level-value/data/gold_per_level_df.csv', index=False)
import requests
import pandas as pd
import os
import time
from datetime import datetime

# Dossier de sortie
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, "data")
os.makedirs(data_folder, exist_ok=True)
output_file = os.path.join(data_folder, "lakers_players.parquet")

# URL et headers NBA
url = "https://stats.nba.com/stats/leagueLeaders"
headers = {
    "Host": "stats.nba.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com"
}

# 5 dernières saisons
current_year = datetime.now().year
seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(current_year-5, current_year)]

# Charger parquet existant
if os.path.exists(output_file):
    df_existing = pd.read_parquet(output_file)
    print(f"Données existantes chargées : {len(df_existing)} lignes")
else:
    df_existing = pd.DataFrame()

# Fonction pour récupérer les stats d'une saison et type
def get_nba_stats(season, season_type):
    params = {
        "LeagueID": "00",
        "PerMode": "PerGame",
        "Season": season,
        "SeasonType": season_type,
        "Scope": "S",
        "StatCategory": "PTS"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        headers_data = data["resultSet"]["headers"]
        rows = data["resultSet"]["rowSet"]
        df = pd.DataFrame(rows, columns=headers_data)
        df["Season"] = season
        df["SeasonType"] = season_type
        # Ajouter image
        df["PLAYER_IMAGE"] = df["PLAYER_ID"].apply(
            lambda pid: f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{pid}.png"
        )
        return df
    except Exception as e:
        print(f"Erreur pour {season} - {season_type}: {e}")
        return None

# Récupérer toutes les saisons
all_dfs = []
for season in seasons:
    for season_type in ["Regular Season", "Playoffs"]:
        print(f"Traitement {season} - {season_type}...")
        df_season = get_nba_stats(season, season_type)
        if df_season is not None:
            # Garder seulement les joueurs Lakers
            df_season = df_season[df_season["TEAM"] == "LAL"]
            if not df_season.empty:
                all_dfs.append(df_season)
        time.sleep(1)

# Concaténer avec l'existant et supprimer doublons exacts
if all_dfs:
    df_new = pd.concat(all_dfs, ignore_index=True)
    if not df_existing.empty:
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.drop_duplicates(subset=["PLAYER_ID", "Season", "SeasonType"], inplace=True)
    df_all.to_parquet(output_file, index=False)
    print(f"✅ Données mises à jour dans {output_file}, total lignes : {len(df_all)}")
else:
    print("⚠ Aucune donnée Lakers récupérée.")

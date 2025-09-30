# Importer les modules
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import os
import time
from datetime import datetime

# Chemin absolu vers le dossier racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Fichier de sortie
output_file = os.path.join(DATA_DIR, "lakers_seasons.parquet")
print("Le fichier sera créé ici :", output_file)

# Définir les saisons NBA (5 dernières saisons)
current_year = datetime.now().year
seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(current_year-5, current_year)]

# Récupérer les équipes NBA et filtrer les Lakers
nba_teams = teams.get_teams()
lakers = [team for team in nba_teams if team["full_name"] == "Los Angeles Lakers"][0]
lakers_id = lakers["id"]

# Charger les données existantes si elles existent
if os.path.exists(output_file):
    df_all_matches = pd.read_parquet(output_file)
    saisons_existantes = df_all_matches["saison"].unique().tolist()
    print(f"Données existantes chargées : {len(df_all_matches)} lignes")
else:
    df_all_matches = pd.DataFrame()
    saisons_existantes = []

# Types de saison
season_types = ["Regular Season", "Playoffs"]

# Récupérer les nouvelles saisons
season_matches = []

for season in seasons:
    saison_label = f"{season[:4]}-{int(season[:4]) + 1}"  # ex: 2020-2021

    if saison_label in saisons_existantes:
        print(f"Saison {saison_label} déjà présente, on passe.")
        continue

    for stype in season_types:
        print(f"Récupération : {saison_label} - {stype}")
        try:
            finder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=lakers_id,
                season_nullable=season,
                season_type_nullable=stype
            )
            df_season = finder.get_data_frames()[0]
            if not df_season.empty:
                df_season["saison"] = saison_label       # Ajouter la colonne saison
                df_season["season_type"] = stype         # Ajouter type de saison
                season_matches.append(df_season)
                print(f"  {len(df_season)} matchs récupérés")
            else:
                print("  Aucun match trouvé")
        except Exception as e:
            print(f"  Erreur : {e}")
        time.sleep(0.2)

# Concaténer et supprimer les doublons
if season_matches:
    df_new = pd.concat(season_matches, ignore_index=True)
    df_all_matches = pd.concat([df_all_matches, df_new], ignore_index=True)
    df_all_matches.drop_duplicates(subset="GAME_ID", inplace=True)
    df_all_matches.to_parquet(output_file, index=False)
    print(f"✅ Données mises à jour : {len(df_all_matches)} lignes au total")
else:
    print("Aucune nouvelle donnée à ajouter")
 
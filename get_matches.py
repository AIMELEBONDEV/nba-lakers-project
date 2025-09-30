from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import os
import time
from datetime import datetime

# -----------------------------
# Paramètres
# -----------------------------
ANNEES = 5
PAUSE = 0.5
OUTPUT_FILE = os.path.join("data", "lakers_players_matches.parquet")

# -----------------------------
# Charger l'historique existant
# -----------------------------
if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
    df_old = pd.read_parquet(OUTPUT_FILE)
    existing_games = set(zip(df_old["PLAYER_ID"], df_old["GAME_ID"]))
    print(f"Historique chargé : {len(df_old)} matchs déjà présents")
else:
    df_old = pd.DataFrame()
    existing_games = set()
    print("Aucun fichier existant, extraction complète.")

# -----------------------------
# Identifier les Lakers
# -----------------------------
nba_teams = teams.get_teams()
lakers = [team for team in nba_teams if team["full_name"] == "Los Angeles Lakers"][0]
lakers_id = lakers["id"]

# -----------------------------
# Récupérer tous les joueurs
# -----------------------------
nba_players = players.get_players()
df_players = pd.DataFrame(nba_players)
df_players.rename(columns={"id": "PLAYER_ID", "full_name": "PLAYER"}, inplace=True)

# -----------------------------
# Définir les saisons
# -----------------------------
current_year = datetime.now().year
seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(current_year-ANNEES, current_year)]

# -----------------------------
# Récupérer les joueurs ayant joué pour les Lakers
# -----------------------------
lakers_players = []
print("Identification des joueurs des Lakers...")
for pid in df_players["PLAYER_ID"]:
    try:
        gamelog = playergamelog.PlayerGameLog(player_id=pid, season=seasons[-1]).get_data_frames()[0]
        if lakers_id in gamelog["TEAM_ID"].values:
            lakers_players.append(pid)
    except:
        pass
    time.sleep(PAUSE)

print(f"{len(lakers_players)} joueurs des Lakers identifiés sur les {ANNEES} dernières saisons.")

# -----------------------------
# Extraction des stats de matchs par joueur avec progression
# -----------------------------
new_data = []
total_jobs = len(lakers_players) * len(seasons)
done_jobs = 0

for i, pid in enumerate(lakers_players, start=1):
    print(f"\n--- Joueur {i}/{len(lakers_players)} (ID {pid}) ---")
    for j, saison in enumerate(seasons, start=1):
        try:
            gamelog = playergamelog.PlayerGameLog(player_id=pid, season=saison).get_data_frames()[0]
            gamelog["PLAYER_ID"] = pid

            # Filtrer les matchs déjà existants
            gamelog_new = gamelog[~gamelog.apply(lambda row: (row["PLAYER_ID"], row["GAME_ID"]) in existing_games, axis=1)]

            if not gamelog_new.empty:
                new_data.append(gamelog_new)
                for _, row in gamelog_new.iterrows():
                    existing_games.add((row["PLAYER_ID"], row["GAME_ID"]))

            print(f"  Saison {saison} ({j}/{len(seasons)}) : {len(gamelog_new)} nouveaux matchs ajoutés")

        except Exception as e:
            print(f"  Erreur pour le joueur {pid}, saison {saison}: {e}")

        done_jobs += 1
        print(f"  Progression globale : {done_jobs}/{total_jobs} ({done_jobs/total_jobs:.1%})")
        time.sleep(PAUSE)

print("\nExtraction terminée.")

# -----------------------------
# Fusion et sauvegarde
# -----------------------------
if new_data:
    df_new = pd.concat(new_data, ignore_index=True)
    df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(subset=["PLAYER_ID", "GAME_ID"])
else:
    df_final = df_old

df_final.to_parquet(OUTPUT_FILE, index=False)
print(f"Total matchs sauvegardés : {len(df_final)}")
print(f"Fichier sauvegardé : {OUTPUT_FILE}")

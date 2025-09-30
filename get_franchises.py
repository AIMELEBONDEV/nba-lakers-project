# Importer les modules nécessaires
from nba_api.stats.static import teams
import pandas as pd
import os

# Récupérer toutes les équipes NBA
nba_teams = teams.get_teams()  # Récupère toutes les équipes
# Construire le DataFrame avec les informations importantes et les logos
franchises = []

for team in nba_teams:
    franchises.append({
        "FRANCHISE_ID": team["id"],
        "NOM": team["full_name"],
        "ABRÉVIATION": team["abbreviation"],
        "VILLE": team["city"],
        "LIEN_LOGO": f"https://cdn.nba.com/logos/nba/{team['id']}/primary/L/logo.svg"
    })

# Créer le DataFrame et sauvegarder en Parquet
df_franchises = pd.DataFrame(franchises)

output_file = os.path.join("data", "franchises.parquet")
df_franchises.to_parquet(output_file, index=False)

print(f"Les données des franchises ont été sauvegardées dans {output_file}")

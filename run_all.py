import subprocess
import sys

# Liste des scripts à exécuter dans l'ordre
scripts = [
    "scripts/get_players.py",
    "scripts/get_franchises.py",
    "scripts/get_matches.py",
    "scripts/get_seasons.py"
]

for i, script in enumerate(scripts, start=1):
    print(f"Lancement du script {i}/{len(scripts)} : {script}")
    try:
        # Exécute le script avec le même interpréteur Python
        subprocess.run([sys.executable, script], check=True)
        print(f"Script {script} terminé avec succès.\n")
    except subprocess.CalledProcessError:
        print(f"Une erreur est survenue lors de l'exécution de {script}.\n")

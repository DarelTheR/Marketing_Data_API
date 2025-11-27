import os
from pathlib import Path
from dotenv import load_dotenv

# Dossier racine des données
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"

# Création des dossiers si besoin
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ======================
#  APIs cinéma
# ======================
load_dotenv()
# TMDb
TMDB_API_KEY: str = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL: str = "https://api.themoviedb.org/3/"

# OMDb
OMDB_API_KEY: str = os.getenv("OMDB_API_KEY")
OMDB_BASE_URL: str = "http://www.omdbapi.com/"

# TVMaze (pas besoin de clé)
TVMAZE_BASE_URL: str = "https://api.tvmaze.com"
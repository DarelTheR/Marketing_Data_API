"""
Module de configuration centralisé pour le projet marketing_ai.
Contient les URLs des APIs, tokens et paramètres globaux.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ======================
#  Dossiers du projet
# ======================
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

# ======================
#  Paramètres généraux
# ======================
TIMEOUT = 10
MAX_ARTICLES = 50
USER_AGENT = "Mozilla/5.0 (compatible; MovieBot/1.0)"

# ======================
#  Paramètres ML
# ======================
RANDOM_STATE = 42
TEST_SIZE = 0.3
TOP_K_RECOMMENDATIONS = 5

# Paramètres TF-IDF
MAX_FEATURES = 500
NGRAM_RANGE = (1, 2)
MIN_DF = 2
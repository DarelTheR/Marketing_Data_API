"""
Module de configuration centralisé pour le projet marketing_ai.
Contient les URLs des APIs, tokens et paramètres globaux.

TODO: À implémenter par la Personne 1 (Data Pipeline)
"""

# URLs des APIs cinéma
APIS = {
    "tmdb": {
        "base_url": "https://api.themoviedb.org/3",
        "endpoints": {
            "movies": "/discover/movie",
            "search": "/search/movie"
        }
    },
    "reddit": {
        "base_url": "https://www.reddit.com",
        "endpoints": {
            "movies": "/r/movies.json",
            "reviews": "/r/moviereviews.json"
        }
    },
    "omdb": {
        "base_url": "http://www.omdbapi.com",
        "params": {
            "apikey": "YOUR_OMDB_API_KEY"
        }
    }
}

# Paramètres généraux
TIMEOUT = 10
MAX_ARTICLES = 50
USER_AGENT = "Mozilla/5.0 (compatible; MovieBot/1.0)"

# Paramètres ML
RANDOM_STATE = 42
TEST_SIZE = 0.3
TOP_K_RECOMMENDATIONS = 5

# Paramètres TF-IDF
MAX_FEATURES = 500
NGRAM_RANGE = (1, 2)
MIN_DF = 2

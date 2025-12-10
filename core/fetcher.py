from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from core import config

logger = logging.getLogger(__name__)


def setup_logger(log_file: Path = Path("logs/marketing.log")) -> None:
    """
    Configure le système de logs (console + fichier).
    À appeler une seule fois au début du programme
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def fetch_with_logging(
    source: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 10,
) -> Optional[Dict[str, Any]]:
    """
    Effectue un GET HTTP avec mesure de la latence et logging.

    :param source: nom de la source (tmdb, omdb, tvmaze)
    :param url: URL complète
    :param params: paramètres query string (dict)
    :param timeout: timeout en secondes
    :return: dictionnaire JSON ou None en cas d’erreur
    """
    start = time.time()
    try:
        response = requests.get(url, params=params, timeout=timeout)
        latency = time.time() - start

        logger.info(
            "FETCH %s - %s - status=%s latency=%.3fs",
            source,
            response.url,
            response.status_code,
            latency,
        )

        if not response.ok:
            logger.warning("Réponse non OK de %s: %s", source, response.text[:200])
            return None

        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("JSON invalide reçu depuis %s", source)
            return None

    except requests.RequestException as e:
        latency = time.time() - start
        logger.error("Erreur de requête %s après %.3fs : %s", source, latency, e)
        return None


def save_raw_json(data: Any, filename: str) -> Path:
    """
    Sauvegarde les données brutes dans data/raw/ au format JSON.

    :param data: objet sérialisable en JSON
    :param filename: nom du fichier (ex: 'tmdb_trending_raw.json')
    :return: chemin du fichier créé
    """
    path = config.RAW_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("Données brutes sauvegardées dans %s", path)
    return path


# ==============================
#   TMDb - Trending movies
# ==============================

def fetch_tmdb_trending(pages: int = 1) -> List[Dict[str, Any]]:
    """
    Récupère des films 'trending' depuis TMDb sur plusieurs pages.

    :param pages: nombre de pages à récupérer
    :return: liste de films (JSON brut TMDb)
    """
    if not config.TMDB_API_KEY:
        logger.error("TMDB_API_KEY manquante (None). Vérifie ton fichier .env.")
        return []

    all_results: List[Dict[str, Any]] = []

    base = config.TMDB_BASE_URL.rstrip("/")  # au cas où il y ait un / final
    for page in range(1, pages + 1):
        url = f"{base}/trending/movie/week"
        params = {
            "api_key": config.TMDB_API_KEY,
            "page": page,
            "language": "en-US",
        }
        data = fetch_with_logging("tmdb", url, params=params)
        if data and "results" in data:
            all_results.extend(data["results"])

    save_raw_json(all_results, "tmdb_trending_raw.json")
    return all_results


# ==============================
#   OMDb - Films par titre
# ==============================

def fetch_omdb_titles(titles: List[str]) -> List[Dict[str, Any]]:
    """
    Récupère des infos de films OMDb à partir d'une liste de titres.

    :param titles: liste de titres à interroger
    :return: liste de réponses JSON OMDb
    """
    if not config.OMDB_API_KEY:
        logger.error("OMDB_API_KEY manquante (None). Vérifie ton fichier .env.")
        return []

    results: List[Dict[str, Any]] = []
    base = config.OMDB_BASE_URL.rstrip("/")

    for title in titles:
        params = {
            "apikey": config.OMDB_API_KEY,
            "t": title,
            "plot": "full",
        }
        data = fetch_with_logging("omdb", base, params=params)
        if data:
            results.append(data)

    save_raw_json(results, "omdb_titles_raw.json")
    return results


# ==============================
#   TVMaze - Shows par ID
# ==============================

def fetch_tvmaze_shows(show_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Récupère des shows TVMaze à partir d'une liste d'IDs.

    :param show_ids: liste d'identifiants de séries
    :return: liste de réponses JSON TVMaze
    """
    results: List[Dict[str, Any]] = []
    base = config.TVMAZE_BASE_URL.rstrip("/")

    for show_id in show_ids:
        url = f"{base}/shows/{show_id}"
        data = fetch_with_logging("tvmaze", url)
        if data:
            results.append(data)

    save_raw_json(results, "tvmaze_shows_raw.json")
    return results


# ==============================
#   Orchestration globale
# ==============================

def run_all_fetchers() -> None:
    """
    Lance l'ensemble des collectes (TMDb, OMDb, TVMaze).
    Collecte aussi les statistiques des appels API.
    """
    logger.info("=== Début de la collecte API ===")
    
    # Variables pour stocker les stats
    all_latencies = []
    all_status_codes = []
    all_timestamps = []
    
    # TMDb - 2 pages
    logger.info("Collecte TMDb...")
    tmdb_start = time.time()
    tmdb_data = fetch_tmdb_trending(pages=2)
    tmdb_latency = time.time() - tmdb_start
    all_latencies.append(tmdb_latency)
    all_status_codes.append(200 if tmdb_data else 500)  # 200 si succès, 500 si échec
    all_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("TMDb: %d éléments récupérés", len(tmdb_data))
    
    # OMDb - Plusieurs titres
    logger.info("Collecte OMDb...")
    omdb_titles = [
        "Inception",
        "The Matrix",
        "Fight Club",
        "Interstellar",
        "The Godfather",
    ]
    omdb_start = time.time()
    omdb_data = fetch_omdb_titles(omdb_titles)
    omdb_latency = time.time() - omdb_start
    all_latencies.append(omdb_latency)
    all_status_codes.append(200 if omdb_data else 500)
    all_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("OMDb: %d éléments récupérés", len(omdb_data))
    
    # TVMaze - IDs qu'on va fetch pour la démo
    logger.info("Collecte TVMaze...")
    tvmaze_ids = [1, 82, 431, 169, 143]
    tvmaze_start = time.time()
    tvmaze_data = fetch_tvmaze_shows(tvmaze_ids)
    tvmaze_latency = time.time() - tvmaze_start
    all_latencies.append(tvmaze_latency)
    all_status_codes.append(200 if tvmaze_data else 500)
    all_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("TVMaze: %d éléments récupérés", len(tvmaze_data))
    
    # Créer le dictionnaire de statistiques
    api_stats = {
        "latencies": all_latencies,
        "status_codes": all_status_codes,
        "timestamps": all_timestamps,
        "sources_count": {
            "tmdb": len(tmdb_data),
            "omdb": len(omdb_data),
            "tvmaze": len(tvmaze_data)
        }
    }
    
    # Sauvegarder les stats dans un fichier JSON
    stats_path = config.RAW_DIR / "api_stats.json"
    with stats_path.open("w", encoding="utf-8") as f:
        json.dump(api_stats, f, indent=2, ensure_ascii=False)
    logger.info(f"Stats API sauvegardées : {stats_path}")
    
    logger.info("=== Collecte terminée ===")
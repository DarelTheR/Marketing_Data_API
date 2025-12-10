from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from core import config

logger = logging.getLogger(__name__)

# Dossier des données nettoyées
PROCESSED_DIR = config.DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ============ Stopwords ============

FR_STOPWORDS = {
    "et", "ou", "les", "des", "de", "du", "la", "le", "un", "une", "au", "aux",
    "en", "dans", "pour", "par", "avec", "ce", "ces", "ceci", "cela", "ça",
    "sur", "sous", "ne", "pas", "plus", "moins", "comme", "que", "qui",
    "dont", "où", "quand", "mais", "car", "donc", "or", "ni", "si",
}

STOPWORDS = set(ENGLISH_STOP_WORDS) | FR_STOPWORDS

HTML_TAG_RE = re.compile(r"<.*?>", flags=re.DOTALL)
PUNCTUATION_RE = re.compile(r"[^\w\s]", flags=re.UNICODE)
MULTISPACE_RE = re.compile(r"\s+")


def load_json(path: Path) -> Any:
    """Charge un fichier JSON et renvoie l'objet Python correspondant."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    """
    Nettoie le texte :
    - minuscules
    - suppression HTML
    - suppression ponctuation
    - normalisation des espaces
    - suppression des stopwords EN/FR
    """
    if not text:
        return ""

    # HTML -> texte brut
    text = HTML_TAG_RE.sub(" ", text)

    # minuscules
    text = text.lower()

    # ponctuation
    text = PUNCTUATION_RE.sub(" ", text)

    # espaces multiples
    text = MULTISPACE_RE.sub(" ", text).strip()

    # stopwords
    tokens = [tok for tok in text.split() if tok not in STOPWORDS]
    return " ".join(tokens)


# ==============================
#   Parsing TMDb
# ==============================

def parse_tmdb(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforme la liste brute TMDb en liste d'enregistrements standardisés.
    """
    records: List[Dict[str, Any]] = []

    for item in raw_data:
        title = item.get("title") or item.get("name") or ""
        overview = item.get("overview") or ""
        language = item.get("original_language") or "unk"
        tmdb_id = item.get("id")

        raw_text = f"{title}. {overview}".strip()

        record = {
            "id": f"tmdb_{tmdb_id}" if tmdb_id is not None else None,
            "source": "tmdb",
            "title": title,
            "raw_text": raw_text,
            "clean_text": normalize_text(raw_text),
            "language": language,
        }
        records.append(record)

    logger.info("TMDb nettoyé : %d enregistrements", len(records))
    return records


# ==============================
#   Parsing OMDb
# ==============================

def parse_omdb(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforme la liste brute OMDb en liste d'enregistrements standardisés.
    """
    records: List[Dict[str, Any]] = []

    for item in raw_data:
        title = item.get("Title") or ""
        plot = item.get("Plot") or ""
        year = item.get("Year") or ""
        omdb_id = item.get("imdbID") or ""

        raw_text = f"{title} ({year}). {plot}".strip()

        record = {
            "id": f"omdb_{omdb_id}" if omdb_id else None,
            "source": "omdb",
            "title": title,
            "raw_text": raw_text,
            "clean_text": normalize_text(raw_text),
            "language": "en",  # OMDb principalement en anglais
        }
        records.append(record)

    logger.info("OMDb nettoyé : %d enregistrements", len(records))
    return records


# ==============================
#   Parsing TVMaze
# ==============================

def parse_tvmaze(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforme la liste brute TVMaze en liste d'enregistrements standardisés.
    """
    records: List[Dict[str, Any]] = []

    for item in raw_data:
        title = item.get("name") or ""
        summary = item.get("summary") or ""  # souvent en HTML
        tvmaze_id = item.get("id")
        language = item.get("language") or "unk"

        raw_text = f"{title}. {summary}".strip()

        record = {
            "id": f"tvmaze_{tvmaze_id}" if tvmaze_id is not None else None,
            "source": "tvmaze",
            "title": title,
            "raw_text": raw_text,
            "clean_text": normalize_text(raw_text),
            "language": language.lower(),
        }
        records.append(record)

    logger.info("TVMaze nettoyé : %d enregistrements", len(records))
    return records


# ==============================
#   Orchestration cleaning
# ==============================

def build_clean_dataset() -> List[Dict[str, Any]]:
    """
    Charge les JSON bruts depuis data/raw/, les standardise et les fusionne
    en une liste unique d'enregistrements nettoyer.
    """
    all_records: List[Dict[str, Any]] = []

    # TMDb
    tmdb_path = config.RAW_DIR / "tmdb_trending_raw.json"
    if tmdb_path.exists():
        tmdb_raw = load_json(tmdb_path)
        if isinstance(tmdb_raw, list):
            all_records.extend(parse_tmdb(tmdb_raw))
        else:
            logger.warning("Format inattendu pour %s (attendu: liste)", tmdb_path)
    else:
        logger.warning("Fichier TMDb brut introuvable : %s", tmdb_path)

    # OMDb
    omdb_path = config.RAW_DIR / "omdb_titles_raw.json"
    if omdb_path.exists():
        omdb_raw = load_json(omdb_path)
        if isinstance(omdb_raw, list):
            all_records.extend(parse_omdb(omdb_raw))
        else:
            logger.warning("Format inattendu pour %s (attendu: liste)", omdb_path)
    else:
        logger.warning("Fichier OMDb brut introuvable : %s", omdb_path)

    # TVMaze
    tvmaze_path = config.RAW_DIR / "tvmaze_shows_raw.json"
    if tvmaze_path.exists():
        tvmaze_raw = load_json(tvmaze_path)
        if isinstance(tvmaze_raw, list):
            all_records.extend(parse_tvmaze(tvmaze_raw))
        else:
            logger.warning("Format inattendu pour %s (attendu: liste)", tvmaze_path)
    else:
        logger.warning("Fichier TVMaze brut introuvable : %s", tvmaze_path)

    logger.info("Total enregistrements nettoyés : %d", len(all_records))
    return all_records


def run_cleaning() -> Path:
    """
    Pipeline de nettoyage : lit les données brutes, nettoie le texte,
    et sauvegarde un fichier JSON unique dans data/processed/clean_data.json
    """
    records = build_clean_dataset()
    
    # Format original (pour Lyes/analyse)
    out_path = PROCESSED_DIR / "clean_data.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    # Format pour ML (pour Ruben)
    ml_path = PROCESSED_DIR / "clean_data_ml.json"
    save_for_ml_pipeline(records, ml_path)
    
    return out_path

def save_for_ml_pipeline(records: List[Dict], output_path: Path) -> None:
    """
    Sauvegarde au format attendu par le pipeline ML (Ruben).
    """
    ml_format = {
        "texts": [r["clean_text"] for r in records],
        "sources": [r["source"] for r in records],
        "titles": [r["title"] for r in records]
    }
    
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(ml_format, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Format ML sauvegardé : {output_path}")
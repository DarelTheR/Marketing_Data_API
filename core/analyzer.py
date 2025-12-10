from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

from core import config

logger = logging.getLogger(__name__)

# Dossiers pour les données traitées et les rapports
PROCESSED_DIR = config.DATA_DIR / "processed"
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_clean_data(path: Path | None = None) -> pd.DataFrame:
    """
    Charge le fichier clean_data.json (liste de dicts) en DataFrame pandas.
    """
    if path is None:
        path = PROCESSED_DIR / "clean_data.json"

    if not path.exists():
        raise FileNotFoundError(f"Fichier de données nettoyées introuvable : {path}")

    with path.open("r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)

    df = pd.DataFrame(data)
    logger.info("clean_data chargé : %d lignes, %d colonnes", df.shape[0], df.shape[1])
    return df


def compute_basic_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcule les indicateurs descriptifs de base sur le dataset.
    """
    # Longueurs de texte
    df["raw_len"] = df["raw_text"].fillna("").str.len()
    df["clean_len"] = df["clean_text"].fillna("").str.len()

    kpis: Dict[str, Any] = {
        "n_documents": int(len(df)),
        "sources_counts": df["source"].value_counts().to_dict(),
        "languages_counts": df["language"].value_counts().to_dict(),
        "avg_raw_length": float(df["raw_len"].mean()),
        "avg_clean_length": float(df["clean_len"].mean()),
        "median_clean_length": float(df["clean_len"].median()),
        "min_clean_length": int(df["clean_len"].min()),
        "max_clean_length": int(df["clean_len"].max()),
    }

    logger.info("KPIs de base calculés.")
    return kpis


def compute_keyword_frequencies(
    df: pd.DataFrame, top_n: int = 100
) -> pd.DataFrame:
    """
    Calcule les fréquences de mots sur la colonne clean_text
    et renvoie un DataFrame (keyword, count).
    """
    texts = df["clean_text"].fillna("").tolist()

    all_tokens: List[str] = " ".join(texts).split()

    counter = Counter(all_tokens)
    most_common: List[Tuple[str, int]] = counter.most_common(top_n)

    keywords_df = pd.DataFrame(most_common, columns=["keyword", "count"])
    logger.info("Top %d mots-clés calculés.", top_n)
    return keywords_df


def save_summary_json(kpis: Dict[str, Any], keywords_df: pd.DataFrame) -> Path:
    """
    Sauvegarde un fichier summary.json avec les KPIs + top mots-clés.
    """
    summary_path = REPORTS_DIR / "summary.json"

    # On peut stocker les 20 premiers mots-clés dans le résumé
    top_keywords = (
        keywords_df.head(20)
        .set_index("keyword")["count"]
        .to_dict()
    )

    summary: Dict[str, Any] = dict(kpis)
    summary["top_keywords"] = top_keywords

    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    logger.info("summary.json sauvegardé : %s", summary_path)
    return summary_path


def save_keywords_csv(keywords_df: pd.DataFrame) -> Path:
    """
    Sauvegarde le DataFrame des mots-clés dans reports/keywords.csv.
    """
    keywords_path = REPORTS_DIR / "keywords.csv"
    keywords_df.to_csv(keywords_path, index=False, encoding="utf-8")
    logger.info("keywords.csv sauvegardé : %s", keywords_path)
    return keywords_path


def run_analysis() -> Tuple[Path, Path]:
    """
    Pipeline complet d'analyse :
    - charge clean_data.json
    - calcule KPIs
    - calcule top mots-clés
    - sauvegarde summary.json et keywords.csv
    """
    logger.info("=== Début de l'analyse (analyzer) ===")
    df = load_clean_data()

    kpis = compute_basic_kpis(df)
    keywords_df = compute_keyword_frequencies(df, top_n=100)

    summary_path = save_summary_json(kpis, keywords_df)
    keywords_path = save_keywords_csv(keywords_df)

    logger.info("=== Analyse terminée ===")
    return summary_path, keywords_path

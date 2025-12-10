"""
Module d'analyse descriptive des données.
Calcule les KPIs et statistiques sur les données collectées.

TODO: À implémenter par la Personne 3 (Analytics & Viz)
"""

import json
import pandas as pd
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def calculate_basic_stats(clean_data):
    """
    Calcule les statistiques de base sur les données.
    
    Args:
        clean_data (dict): Données nettoyées
        
    Returns:
        dict: Statistiques descriptives
    """
    # TODO: Implémenter les calculs d'analyse
    texts = clean_data['texts']
    sources = clean_data['sources']
    
    stats = {
        'total_texts': len(texts),
        'avg_text_length': sum(len(text.split()) for text in texts) / len(texts),
        'sources_distribution': dict(Counter(sources)),
        'total_words': sum(len(text.split()) for text in texts)
    }
    
    logger.info(f"Statistiques calculées pour {stats['total_texts']} textes")
    return stats

def extract_top_keywords(texts, top_n=20):
    """
    Extrait les mots-clés les plus fréquents.
    
    Args:
        texts (list): Liste des textes
        top_n (int): Nombre de mots-clés à retourner
        
    Returns:
        list: Liste des top mots-clés avec fréquences
    """
    # TODO: Implémenter l'extraction complète
    all_words = ' '.join(texts).split()
    word_counts = Counter(all_words)
    top_keywords = word_counts.most_common(top_n)
    
    logger.info(f"Top {top_n} mots-clés extraits")
    return top_keywords

def create_summary_json(clean_data, api_stats=None):
    """
    Crée le fichier summary.json avec tous les KPIs.
    
    Args:
        clean_data (dict): Données nettoyées
        api_stats (dict): Statistiques des APIs
        
    Returns:
        dict: Résumé complet
    """
    stats = calculate_basic_stats(clean_data)
    keywords = extract_top_keywords(clean_data['texts'])
    
    summary = {
        'metadata': {
            'theme': 'cinema',
            'collection_date': '2024-11-27',
            'total_texts': stats['total_texts']
        },
        'statistics': stats,
        'top_keywords': keywords[:10],
        'api_performance': api_stats or {}
    }
    
    # Sauvegarder
    with open('reports/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info("Summary.json créé")
    return summary

def create_keywords_csv(texts, filepath='reports/keywords.csv'):
    """
    Crée le fichier CSV des mots-clés.
    
    Args:
        texts (list): Liste des textes
        filepath (str): Chemin de sauvegarde
    """
    # TODO: Implémenter la création du CSV
    keywords = extract_top_keywords(texts, 50)
    
    # Créer un DataFrame simple
    df = pd.DataFrame(keywords, columns=['keyword', 'frequency'])
    df.to_csv(filepath, index=False)
    
    logger.info(f"Keywords CSV créé: {filepath}")

def main():
    """Test du module d'analyse."""
    # Charger les données
    with open('data/processed/clean_data.json', 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    # Analyser
    summary = create_summary_json(clean_data)
    create_keywords_csv(clean_data['texts'])
    
    print(f"Analyse terminée: {summary['metadata']['total_texts']} textes")

if __name__ == "__main__":
    main()

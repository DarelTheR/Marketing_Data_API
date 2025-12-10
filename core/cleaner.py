"""
Module de nettoyage et pré-traitement de texte.
Gère la normalisation, stopwords et lemmatisation.

TODO: À implémenter par la Personne 1 (Data Pipeline)
"""

import re
import json
import logging
# import nltk  # À installer si pas déjà fait
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)

def clean_text(text):
    """
    Nettoie un texte individuel.
    
    Args:
        text (str): Texte brut à nettoyer
        
    Returns:
        str: Texte nettoyé
    """
    # TODO: Implémenter le nettoyage complet
    # - Minuscules
    # - Suppression ponctuation
    # - Suppression stopwords FR/EN
    # - Optionnel: lemmatisation
    
    # Version simplifiée temporaire
    if not text:
        return ""
    
    # Minuscules et nettoyage basique
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Supprime ponctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Normalise espaces
    
    return text

def process_raw_data(raw_data):
    """
    Traite les données brutes de toutes les sources.
    
    Args:
        raw_data (dict): Données brutes des APIs
        
    Returns:
        dict: Données nettoyées au format standardisé
    """
    logger.info("Début du nettoyage des données...")
    
    # TODO: Implémenter le traitement complet
    # Pour l'instant, charge les données mock
    
    with open('data/processed/clean_data.json', 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    logger.info(f"Données nettoyées: {len(clean_data['texts'])} textes")
    return clean_data

def save_clean_data(clean_data, filepath='data/processed/clean_data.json'):
    """
    Sauvegarde les données nettoyées.
    
    Args:
        clean_data (dict): Données nettoyées
        filepath (str): Chemin de sauvegarde
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Données sauvegardées: {filepath}")

def main():
    """Test du module de nettoyage."""
    # TODO: Implémenter les tests
    from .fetcher import fetch_all_sources
    
    raw_data = fetch_all_sources()
    clean_data = process_raw_data(raw_data)
    save_clean_data(clean_data)
    
    print(f"Nettoyage terminé: {len(clean_data['texts'])} textes")

if __name__ == "__main__":
    main()

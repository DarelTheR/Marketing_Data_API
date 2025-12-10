"""
Module de vectorisation des features pour le machine learning.
Transforme les textes nettoyés en représentations numériques via TF-IDF.
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_clean_data(filepath='data/processed/clean_data_ml.json'):
    """
    Charge les données nettoyées depuis le fichier JSON.
    
    Args:
        filepath (str): Chemin vers le fichier de données nettoyées
        
    Returns:
        tuple: (texts, sources, titles) - listes des textes, sources et titres
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        texts = data['texts']
        sources = data['sources'] 
        titles = data['titles']
        
        logger.info(f"Données chargées: {len(texts)} textes de {len(set(sources))} sources")
        return texts, sources, titles
        
    except FileNotFoundError:
        logger.error(f"Fichier {filepath} non trouvé")
        raise
    except KeyError as e:
        logger.error(f"Clé manquante dans les données: {e}")
        raise

def create_tfidf_features(texts, max_features=500, ngram_range=(1, 2), min_df=2):
    """
    Crée la matrice de features TF-IDF à partir des textes.
    
    Args:
        texts (list): Liste des textes nettoyés
        max_features (int): Nombre maximum de features
        ngram_range (tuple): Range des n-grammes (ex: (1,2) = mots seuls + bigrammes)
        min_df (int): Fréquence minimale d'un terme pour être inclus
        
    Returns:
        tuple: (feature_matrix, vectorizer) - matrice sparse et vectorizer entraîné
    """
    logger.info("Création de la matrice TF-IDF...")
    
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        min_df=min_df,
        stop_words='english',
        lowercase=True,
        strip_accents='ascii'
    )
    
    # Transformation des textes en matrice TF-IDF
    X = vectorizer.fit_transform(texts)
    
    logger.info(f"Matrice TF-IDF créée: {X.shape[0]} documents x {X.shape[1]} features")
    logger.info(f"Densité de la matrice: {X.nnz / (X.shape[0] * X.shape[1]):.4f}")
    
    return X, vectorizer

def save_features_and_vectorizer(X, vectorizer, 
                                features_path='data/processed/features.npz',
                                vectorizer_path='data/models/vectorizer.pkl'):
    """
    Sauvegarde la matrice de features et le vectorizer.
    
    Args:
        X: Matrice sparse des features
        vectorizer: Vectorizer TF-IDF entraîné
        features_path (str): Chemin pour sauvegarder les features
        vectorizer_path (str): Chemin pour sauvegarder le vectorizer
    """
    # Créer le dossier s'il n'existe pas
    import os
    os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
    os.makedirs(os.path.dirname(features_path), exist_ok=True)
    """
    Sauvegarde la matrice de features et le vectorizer.
    
    Args:
        X: Matrice sparse des features
        vectorizer: Vectorizer TF-IDF entraîné
        features_path (str): Chemin pour sauvegarder les features
        vectorizer_path (str): Chemin pour sauvegarder le vectorizer
    """
    # Sauvegarde des features (format sparse)
    from scipy.sparse import save_npz
    save_npz(features_path, X)
    logger.info(f"Features sauvegardées: {features_path}")
    
    # Sauvegarde du vectorizer
    joblib.dump(vectorizer, vectorizer_path)
    logger.info(f"Vectorizer sauvegardé: {vectorizer_path}")

def get_top_features(vectorizer, n_features=20):
    """
    Récupère les top features (mots) les plus importants.
    
    Args:
        vectorizer: Vectorizer TF-IDF entraîné
        n_features (int): Nombre de features à récupérer
        
    Returns:
        list: Liste des top features/mots
    """
    feature_names = vectorizer.get_feature_names_out()
    
    # Pour cet exemple, on prend juste les premiers
    # Dans un vrai cas, on pourrait calculer les scores moyens
    top_features = feature_names[:n_features].tolist()
    
    logger.info(f"Top {n_features} features: {top_features[:5]}...")
    return top_features

def main():
    """Fonction principale pour tester le module features."""
    try:
        # Chargement des données
        texts, sources, titles = load_clean_data()
        
        # Création des features TF-IDF
        X, vectorizer = create_tfidf_features(texts)
        
        # Sauvegarde
        save_features_and_vectorizer(X, vectorizer)
        
        # Affichage des top features
        top_features = get_top_features(vectorizer)
        print(f"Top features: {top_features}")
        
        logger.info("Module features exécuté avec succès !")
        
    except Exception as e:
        logger.error(f"Erreur dans le module features: {e}")
        raise

if __name__ == "__main__":
    main()

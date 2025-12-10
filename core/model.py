"""
Module de machine learning pour la classification et le clustering de films.
Implémente clustering K-Means et classification supervisée.
"""

import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, accuracy_score, classification_report
import joblib
import logging
from collections import Counter

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_clustering(X, n_clusters=5, random_state=42):
    """
    Entraîne un modèle de clustering K-Means.
    
    Args:
        X: Matrice de features (TF-IDF)
        n_clusters (int): Nombre de clusters
        random_state (int): Seed pour reproductibilité
        
    Returns:
        tuple: (model, predictions, silhouette_score)
    """
    logger.info(f"Entraînement K-Means avec {n_clusters} clusters...")
    
    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=20,
        max_iter=500
    )
    
    # Entraînement et prédictions
    predictions = model.fit_predict(X)
    
    # Calcul du score de qualité
    if len(set(predictions)) > 1:  # Au moins 2 clusters
        sil_score = silhouette_score(X, predictions)
    else:
        sil_score = 0.0
    
    logger.info(f"Clustering terminé. Silhouette score: {sil_score:.3f}")
    logger.info(f"Distribution des clusters: {Counter(predictions)}")
    
    return model, predictions, sil_score

def create_pseudo_labels(sources):
    """
    Crée des pseudo-labels pour la classification basés sur les sources.
    Utile pour tester la classification supervisée.
    
    Args:
        sources (list): Liste des sources ("tmdb", "reddit", "omdb")
        
    Returns:
        list: Liste de labels numériques
    """
    label_mapping = {"tmdb": 0, "reddit": 1, "omdb": 2}
    labels = [label_mapping.get(source, 0) for source in sources]
    
    logger.info(f"Pseudo-labels créés: {Counter(labels)}")
    return labels

def train_classification(X, y, test_size=0.3, random_state=42):
    """
    Entraîne un modèle de classification supervisée.
    
    Args:
        X: Matrice de features
        y: Labels de classification
        test_size (float): Proportion du jeu de test
        random_state (int): Seed pour reproductibilité
        
    Returns:
        dict: Résultats avec modèle, prédictions et métriques
    """
    logger.info("Entraînement de la classification...")
    
    # Division train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Modèle de classification
    model = LogisticRegression(
        random_state=random_state,
        max_iter=1000,
        multi_class='ovr'
    )
    
    # Entraînement
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Métriques
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    logger.info(f"Classification terminée. Accuracy: {accuracy:.3f}")
    
    results = {
        'model': model,
        'accuracy': accuracy,
        'classification_report': report,
        'predictions': [int(p) for p in y_pred],
        'test_labels': [int(p) for p in y_test] 
    }
    
    return results

def analyze_clusters(predictions, titles, texts, n_top_words=5):
    """
    Analyse le contenu des clusters pour comprendre leur signification.
    
    Args:
        predictions (array): Prédictions de clustering
        titles (list): Titres des films
        texts (list): Textes des films
        n_top_words (int): Nombre de mots top par cluster
        
    Returns:
        dict: Analyse des clusters
    """
    cluster_analysis = {}
    
    for cluster_id in set(predictions):
        # Films dans ce cluster
        cluster_indices = [i for i, pred in enumerate(predictions) if pred == cluster_id]
        cluster_titles = [titles[i] for i in cluster_indices]
        cluster_texts = [texts[i] for i in cluster_indices]
        
        # Mots les plus fréquents dans ce cluster
        all_words = ' '.join(cluster_texts).split()
        word_counts = Counter(all_words)
        top_words = [word for word, count in word_counts.most_common(n_top_words)]
        
        cluster_analysis[f"cluster_{cluster_id}"] = {
            'titles': cluster_titles,
            'top_words': top_words,
            'size': len(cluster_titles)
        }
    
    logger.info(f"Analyse des clusters terminée pour {len(cluster_analysis)} clusters")
    return cluster_analysis

def save_model_and_results(model, model_type, results, 
                          model_path='data/models/model.pkl',
                          results_path='data/processed/ml_results.json'):
    """
    Sauvegarde le modèle et les résultats.
    
    Args:
        model: Modèle ML entraîné
        model_type (str): Type de modèle ("clustering" ou "classification")
        results (dict): Résultats à sauvegarder
        model_path (str): Chemin de sauvegarde du modèle
        results_path (str): Chemin de sauvegarde des résultats
    """
    # Sauvegarde du modèle
    joblib.dump(model, model_path)
    logger.info(f"Modèle sauvegardé: {model_path}")
    
    # Préparation des résultats pour JSON (conversion des numpy arrays)
    json_results = {
        'model_type': model_type,
        **results
    }
    
    # Conversion des arrays numpy en listes pour JSON
    for key, value in json_results.items():
        if isinstance(value, np.ndarray):
            json_results[key] = value.tolist()
    
    # Sauvegarde des résultats
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Résultats sauvegardés: {results_path}")

def main():
    """Fonction principale pour tester le module ML."""
    try:
        # Import du module features pour charger les données
        import sys
        sys.path.append('.')
        from core.features import load_clean_data, create_tfidf_features
        
        # Chargement des données
        texts, sources, titles = load_clean_data()
        
        # Création des features
        X, vectorizer = create_tfidf_features(texts)
        
        # OPTION 1: CLUSTERING (non-supervisé)
        logger.info("=== CLUSTERING K-MEANS ===")
        clustering_model, predictions, sil_score = train_clustering(X, n_clusters=4)
        
        # Analyse des clusters
        cluster_analysis = analyze_clusters(predictions, titles, texts)
        
        # Résultats clustering
        clustering_results = {
            'predictions': predictions.tolist() if hasattr(predictions, 'tolist') else list(predictions),
            'silhouette_score': sil_score,
            'n_clusters': 4,
            'cluster_analysis': cluster_analysis
        }
        
        # Sauvegarde clustering
        save_model_and_results(clustering_model, 'clustering', clustering_results)
        
        # OPTION 2: CLASSIFICATION (supervisée avec pseudo-labels)
        logger.info("\n=== CLASSIFICATION SUPERVISÉE ===")
        pseudo_labels = create_pseudo_labels(sources)
        classification_results = train_classification(X, pseudo_labels)
        
        # Affichage des résultats
        print("\n=== RÉSULTATS CLUSTERING ===")
        for cluster, info in cluster_analysis.items():
            print(f"{cluster}: {info['titles']} (mots-clés: {info['top_words']})")
        
        print(f"\nSilhouette Score: {sil_score:.3f}")
        print(f"Classification Accuracy: {classification_results['accuracy']:.3f}")
        
        logger.info("Module ML exécuté avec succès !")
        
    except Exception as e:
        logger.error(f"Erreur dans le module ML: {e}")
        raise

if __name__ == "__main__":
    main()

"""
Module de recommandation basé sur la similarité cosinus.
Permet de trouver des films similaires à partir d'une requête textuelle.
"""

import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_models_and_data(vectorizer_path='data/models/vectorizer.pkl'):
    """
    Charge le vectorizer et les données nécessaires pour la recommandation.
    
    Args:
        vectorizer_path (str): Chemin vers le vectorizer sauvegardé
        
    Returns:
        tuple: (vectorizer, texts, titles) pour les recommandations
    """
    try:
        # Charger le vectorizer
        vectorizer = joblib.load(vectorizer_path)
        
        # Charger les données clean
        with open('data/processed/clean_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        texts = data['texts']
        titles = data['titles']
        
        logger.info(f"Modèles chargés: {len(texts)} films disponibles")
        return vectorizer, texts, titles
        
    except FileNotFoundError as e:
        logger.error(f"Fichier non trouvé: {e}")
        raise

def find_similar_movies(query_text, vectorizer, texts, titles, top_k=5):
    """
    Trouve les films les plus similaires à une requête textuelle.
    
    Args:
        query_text (str): Texte de recherche (ex: "epic space adventure")
        vectorizer: Vectorizer TF-IDF entraîné
        texts (list): Liste des textes de films
        titles (list): Liste des titres de films
        top_k (int): Nombre de recommandations à retourner
        
    Returns:
        list: Liste de tuples (titre, score_similarité)
    """
    logger.info(f"Recherche de films similaires à: '{query_text}'")
    
    # Vectoriser la requête
    query_vector = vectorizer.transform([query_text.lower()])
    
    # Vectoriser tous les textes de films
    films_vectors = vectorizer.transform(texts)
    
    # Calculer la similarité cosinus
    similarities = cosine_similarity(query_vector, films_vectors)[0]
    
    # Trouver les indices des films les plus similaires
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    # Créer la liste des recommandations
    recommendations = []
    for idx in top_indices:
        title = titles[idx]
        score = similarities[idx]
        recommendations.append((title, float(score)))
    
    logger.info(f"Top {top_k} recommandations trouvées")
    return recommendations

def recommend_by_genre(cluster_predictions, titles, target_cluster, top_k=3):
    """
    Recommande des films du même cluster/genre.
    
    Args:
        cluster_predictions (list): Prédictions de clustering pour chaque film
        titles (list): Liste des titres de films
        target_cluster (int): Cluster cible
        top_k (int): Nombre de recommandations
        
    Returns:
        list: Liste des titres recommandés
    """
    # Trouver tous les films du cluster cible
    cluster_films = [
        titles[i] for i, cluster in enumerate(cluster_predictions) 
        if cluster == target_cluster
    ]
    
    # Retourner les top_k premiers (ou tous si moins que top_k)
    recommendations = cluster_films[:top_k]
    
    logger.info(f"Recommandations du cluster {target_cluster}: {recommendations}")
    return recommendations

def create_recommendation_report(sample_queries=None):
    """
    Crée un rapport de test avec des exemples de recommandations.
    
    Args:
        sample_queries (list): Liste de requêtes de test
        
    Returns:
        dict: Rapport avec exemples de recommandations
    """
    if sample_queries is None:
        sample_queries = [
            "epic space adventure",
            "funny superhero comedy",
            "scary horror monster",
            "action car racing"
        ]
    
    try:
        vectorizer, texts, titles = load_models_and_data()
        
        report = {
            "total_films": len(titles),
            "sample_recommendations": {}
        }
        
        for query in sample_queries:
            recommendations = find_similar_movies(
                query, vectorizer, texts, titles, top_k=3
            )
            
            report["sample_recommendations"][query] = [
                {"title": title, "similarity_score": score}
                for title, score in recommendations
            ]
        
        # Sauvegarder le rapport
        with open('reports/recommendations_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info("Rapport de recommandations créé")
        return report
        
    except Exception as e:
        logger.error(f"Erreur lors de la création du rapport: {e}")
        return {"error": str(e)}

def main():
    """Fonction principale pour tester le module de recommandation."""
    try:
        # Assurer que les modèles existent (lancer features et model d'abord)
        import sys
        sys.path.append('.')
        from core.features import main as features_main
        from core.model import main as model_main
        
        # Exécuter les modules précédents si nécessaire
        try:
            vectorizer, texts, titles = load_models_and_data()
        except FileNotFoundError:
            logger.info("Génération des modèles manquants...")
            features_main()
            vectorizer, texts, titles = load_models_and_data()
        
        # Tests de recommandation
        print("\n=== SYSTÈME DE RECOMMANDATION ===")
        
        test_queries = [
            "epic space adventure",
            "funny comedy jokes",
            "scary horror monster",
            "superhero action"
        ]
        
        for query in test_queries:
            print(f"\nRecherche: '{query}'")
            recommendations = find_similar_movies(
                query, vectorizer, texts, titles, top_k=3
            )
            
            for i, (title, score) in enumerate(recommendations, 1):
                print(f"  {i}. {title} (similarité: {score:.3f})")
        
        # Créer le rapport de recommandations
        report = create_recommendation_report()
        print(f"\nRapport sauvegardé avec {report.get('total_films', 0)} films")
        
        logger.info("Module de recommandation exécuté avec succès !")
        
    except Exception as e:
        logger.error(f"Erreur dans le module de recommandation: {e}")
        raise

if __name__ == "__main__":
    main()

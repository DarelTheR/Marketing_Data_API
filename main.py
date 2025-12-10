#!/usr/bin/env python3
"""
Orchestrateur principal du projet Marketing AI.
Lance le pipeline complet: collecte → nettoyage → ML → visualisation.
"""

import sys
import os
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/marketing.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas."""
    directories = [
        'data/raw',
        'data/processed', 
        'data/models',
        'reports',
        'figs',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    logger.info("Structure de répertoires vérifiée")

def run_data_pipeline():
    """
    Exécute la partie 1: collecte et nettoyage des données.
    """
    logger.info("=== ÉTAPE 1: PIPELINE DE DONNÉES ===")
    
    try:
        from core import fetcher, cleaner
        
        # Collecte des données brutes
        logger.info("Collecte des données depuis les APIs...")
        fetcher.run_all_fetchers()
        
        # Nettoyage et structuration
        logger.info("Nettoyage et structuration des données...")
        cleaner.run_cleaning()
        
        logger.info("✅ Pipeline de données terminé")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur pipeline de données: {e}")
        return False

def run_ml_pipeline():
    """
    Exécute la partie 2: machine learning et recommandation.
    """
    logger.info("=== ÉTAPE 2: MACHINE LEARNING ===")
    
    try:
        from core import features, model, recommender
        
        # Extraction des features
        logger.info("Extraction des features TF-IDF...")
        texts, sources, titles = features.load_clean_data()
        X, vectorizer = features.create_tfidf_features(texts)
        features.save_features_and_vectorizer(X, vectorizer)
        
        # Entraînement du modèle ML
        logger.info("Entraînement du modèle ML...")
        clustering_model, predictions, sil_score = model.train_clustering(X)
        
        # Analyse des clusters
        cluster_analysis = model.analyze_clusters(predictions, titles, texts)
        
        # Sauvegarde des résultats
        clustering_results = {
            'predictions': [int(p) for p in predictions],
            'silhouette_score': sil_score,
            'n_clusters': len(set(predictions)),
            'cluster_analysis': cluster_analysis
        }
        
        model.save_model_and_results(clustering_model, 'clustering', clustering_results)
        
        # Test du système de recommandation
        logger.info("Test du système de recommandation...")
        recommender.create_recommendation_report()
        
        logger.info("✅ Pipeline ML terminé")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur pipeline ML: {e}")
        return False

def run_analytics_pipeline():
    """
    Exécute la partie 3: analyses et visualisations.
    """
    logger.info("=== ÉTAPE 3: ANALYTICS & VISUALISATION ===")
    
    try:
        from core import viz
        
        # Génération des visualisations
        logger.info("Génération des visualisations...")
        viz.create_all_figures()
        
        logger.info("✅ Pipeline analytics terminé")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur pipeline analytics: {e}")
        return False

def generate_final_report():
    """
    Génère le rapport final du projet.
    """
    logger.info("=== GÉNÉRATION DU RAPPORT FINAL ===")
    
    try:
        # Charger les différents résultats
        import json
        
        with open('reports/summary.json', 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        with open('data/processed/ml_results.json', 'r', encoding='utf-8') as f:
            ml_results = json.load(f)
        
        # Créer le rapport consolidé
        final_report = {
            'project_info': {
                'name': 'Marketing AI - Analyse de Films',
                'completion_date': datetime.now().isoformat(),
                'team': 'Trinôme Data Science'
            },
            'data_summary': summary,
            'ml_results': {
                'model_type': ml_results['model_type'],
                'performance': {
                    'silhouette_score': ml_results['silhouette_score'],
                    'n_clusters': ml_results['n_clusters']
                }
            },
            'deliverables': {
                'models': ['data/models/model.pkl', 'data/models/vectorizer.pkl'],
                'reports': ['reports/summary.json', 'reports/keywords.csv', 'reports/dashboard.pdf'],
                'visualizations': [
                    'figs/sources_bar.png',
                    'figs/top_keywords.png',
                    'figs/latency_box.png', 
                    'figs/status_codes.png',
                    'figs/timeline_activity.png',
                    'figs/ml_clusters.png'
                ]
            }
        }
        
        # Sauvegarder le rapport final
        with open('reports/final_report.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Rapport final généré")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur génération rapport final: {e}")
        return False

def main():
    """
    Fonction principale - orchestre tout le pipeline.
    """
    start_time = datetime.now()
    
    print("🎬 === MARKETING AI - PIPELINE COMPLET ===")
    print(f"Démarrage: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuration initiale
    setup_directories()
    
    # Exécution séquentielle des 3 parties
    success = True
    
    # Partie 1: Data Pipeline (Personne 1)
    if not run_data_pipeline():
        success = False
    
    # Partie 2: Machine Learning (Personne 2) 
    if success and not run_ml_pipeline():
        success = False
    
    # Partie 3: Analytics & Viz (Personne 3)
    if success and not run_analytics_pipeline():
        success = False
    
    # Rapport final
    if success:
        generate_final_report()
    
    # Résumé final
    end_time = datetime.now()
    duration = end_time - start_time
    
    print()
    print("=== RÉSUMÉ D'EXÉCUTION ===")
    print(f"Durée totale: {duration}")
    print(f"Statut: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
    
    if success:
        print("\n📁 Livrables générés:")
        print("- Modèles ML: data/models/")
        print("- Rapports: reports/")
        print("- Visualisations: figs/")
        print("- Logs: logs/marketing.log")
    
    print("\n🎯 Projet Marketing AI terminé!")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
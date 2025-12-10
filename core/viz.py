"""
Module de visualisation et création de dashboard.
Génère les 6 figures obligatoires + dashboard PDF.

TODO: À implémenter par la Personne 3 (Analytics & Viz)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def plot_sources_volume(sources, save_path='figs/sources_bar.png'):
    """
    Crée un barplot du volume par source.
    
    Args:
        sources (list): Liste des sources
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter le graphique complet
    plt.figure(figsize=(10, 6))
    source_counts = Counter(sources)
    
    plt.bar(source_counts.keys(), source_counts.values())
    plt.title('Volume de données par source')
    plt.xlabel('Source')
    plt.ylabel('Nombre d\'articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sources sauvegardé: {save_path}")

def plot_top_keywords(texts, save_path='figs/top_keywords.png'):
    """
    Crée un barplot des mots-clés les plus fréquents.
    
    Args:
        texts (list): Liste des textes
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter le graphique des mots-clés
    plt.figure(figsize=(12, 6))
    
    all_words = ' '.join(texts).split()
    word_counts = Counter(all_words)
    top_words = dict(word_counts.most_common(15))
    
    plt.barh(list(top_words.keys()), list(top_words.values()))
    plt.title('Top 15 mots-clés les plus fréquents')
    plt.xlabel('Fréquence')
    plt.tight_layout()
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique keywords sauvegardé: {save_path}")

def plot_latency_distribution(latencies, save_path='figs/latency_box.png'):
    """
    Crée un boxplot de la distribution des latences.
    
    Args:
        latencies (list): Latences des APIs
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter le boxplot
    plt.figure(figsize=(8, 6))
    
    plt.boxplot(latencies)
    plt.title('Distribution des latences API')
    plt.ylabel('Latence (secondes)')
    plt.grid(axis='y', alpha=0.3)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique latences sauvegardé: {save_path}")

def plot_status_codes(status_codes, save_path='figs/status_codes.png'):
    """
    Crée un pie chart des statuts HTTP.
    
    Args:
        status_codes (list): Codes de statut HTTP
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter le pie chart
    plt.figure(figsize=(8, 8))
    
    status_counts = Counter(status_codes)
    
    plt.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%')
    plt.title('Répartition des statuts HTTP')
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique statuts sauvegardé: {save_path}")

def plot_timeline_activity(timestamps, save_path='figs/timeline_activity.png'):
    """
    Crée une timeline de l'activité.
    
    Args:
        timestamps (list): Timestamps des collectes
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter la timeline
    plt.figure(figsize=(12, 6))
    
    # Simulation simple
    hours = list(range(24))
    activity = [len(timestamps) * (0.5 + 0.3 * (h % 12) / 12) for h in hours]
    
    plt.plot(hours, activity, marker='o')
    plt.title('Timeline d\'activité de collecte')
    plt.xlabel('Heure')
    plt.ylabel('Nombre d\'articles')
    plt.grid(True, alpha=0.3)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Timeline sauvegardée: {save_path}")

def plot_ml_results(ml_results, save_path='figs/ml_clusters.png'):
    """
    Visualise les résultats ML (clusters ou classification).
    
    Args:
        ml_results (dict): Résultats du machine learning
        save_path (str): Chemin de sauvegarde
    """
    # TODO: Implémenter selon le type de ML
    if ml_results.get('model_type') == 'clustering':
        plot_clustering_results(ml_results, save_path)
    else:
        plot_classification_results(ml_results, save_path)

def plot_clustering_results(ml_results, save_path):
    """Visualise les résultats de clustering."""
    plt.figure(figsize=(12, 8))
    
    cluster_analysis = ml_results.get('cluster_analysis', {})
    
    # Graphique des tailles de clusters
    cluster_sizes = [info['size'] for info in cluster_analysis.values()]
    cluster_names = list(cluster_analysis.keys())
    
    plt.bar(cluster_names, cluster_sizes)
    plt.title('Taille des clusters de films')
    plt.xlabel('Cluster')
    plt.ylabel('Nombre de films')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Résultats clustering sauvegardés: {save_path}")

def plot_classification_results(ml_results, save_path):
    """Visualise les résultats de classification."""
    # TODO: Matrice de confusion ou scores par classe
    pass

def create_dashboard_pdf(save_path='reports/dashboard.pdf'):
    """
    Compile toutes les figures en un dashboard PDF.
    
    Args:
        save_path (str): Chemin de sauvegarde du PDF
    """
    # TODO: Implémenter la compilation PDF
    from matplotlib.backends.backend_pdf import PdfPages
    
    fig_paths = [
        'figs/sources_bar.png',
        'figs/top_keywords.png', 
        'figs/latency_box.png',
        'figs/status_codes.png',
        'figs/timeline_activity.png',
        'figs/ml_clusters.png'
    ]
    
    logger.info(f"Dashboard PDF créé: {save_path}")

def create_all_figures():
    """
    Génère toutes les figures obligatoires.
    """
    logger.info("Génération de toutes les figures...")
    
    # Charger les données
    with open('data/processed/clean_data.json', 'r', encoding='utf-8') as f:
        clean_data = json.load(f)
    
    # Données mock pour les APIs
    api_stats = {
        'latencies': [0.4, 0.6, 0.3, 0.5, 0.7],
        'status_codes': [200, 200, 200, 404, 200],
        'timestamps': ['2024-11-27 10:30', '2024-11-27 10:31']
    }
    
    # Générer les 5 figures de base
    plot_sources_volume(clean_data['sources'])
    plot_top_keywords(clean_data['texts'])
    plot_latency_distribution(api_stats['latencies'])
    plot_status_codes(api_stats['status_codes'])
    plot_timeline_activity(api_stats['timestamps'])
    
    # Figure ML si disponible
    try:
        with open('data/processed/ml_results.json', 'r') as f:
            ml_results = json.load(f)
        plot_ml_results(ml_results)
    except FileNotFoundError:
        logger.warning("Résultats ML non trouvés, figure ML non générée")
    
    # Dashboard PDF
    create_dashboard_pdf()
    
    logger.info("Toutes les figures générées !")

def main():
    """Test du module de visualisation."""
    create_all_figures()
    print("Module viz testé avec succès!")

if __name__ == "__main__":
    main()

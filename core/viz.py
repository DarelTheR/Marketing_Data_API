"""
Module de visualisation et création de dashboard.
Génère les 6 figures obligatoires + dashboard PDF.

À IMPLÉMENTER PAR LYES
"""

import matplotlib.pyplot as plt
import json
from collections import Counter
import logging
import os

logger = logging.getLogger(__name__)

def plot_sources_volume(sources, save_path='figs/sources_bar.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_sources_volume")
    pass

def plot_top_keywords(texts, save_path='figs/top_keywords.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_top_keywords")
    pass

def plot_latency_distribution(latencies, save_path='figs/latency_box.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_latency_distribution")
    pass

def plot_status_codes(status_codes, save_path='figs/status_codes.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_status_codes")
    pass

def plot_timeline_activity(timestamps, save_path='figs/timeline_activity.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_timeline_activity")
    pass

def plot_ml_results(ml_results, save_path='figs/ml_clusters.png'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter plot_ml_results")
    pass

def create_dashboard_pdf(save_path='reports/dashboard.pdf'):
    """À implémenter par Lyes."""
    logger.info(f"TODO: Implémenter create_dashboard_pdf")
    pass

def create_all_figures():
    """
    Fonction principale que Lyes implémentera.
    Pour l'instant, elle ne fait rien pour ne pas bloquer le pipeline.
    """
    logger.info("=== Module viz.py - À IMPLÉMENTER PAR LYES ===")
    logger.warning("⚠️  Les visualisations ne sont pas encore générées.")
    logger.warning("⚠️  Lyes doit implémenter les fonctions de ce module.")
    
    # Créer les dossiers même si vides
    os.makedirs('figs', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

def main():
    """Test du module."""
    create_all_figures()
    print("Module viz prêt pour implémentation par Lyes")

if __name__ == "__main__":
    main()
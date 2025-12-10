#!/usr/bin/env python3
"""
Script de test pour la partie 2 (Machine Learning) du projet marketing_ai.
Ce script teste tous les modules ML avec les données mock.
"""

import sys
import os
sys.path.append('.')

from core.features import main as test_features
from core.model import main as test_model  
from core.recommender import main as test_recommender

def main():
    """
    Lance tous les tests de la partie ML.
    """
    print("🎬 === TEST COMPLET PARTIE 2 - MACHINE LEARNING ===\n")
    
    try:
        print("📊 1. Test du module Features (TF-IDF)...")
        test_features()
        print("✅ Module Features OK!\n")
        
        print("🤖 2. Test du module Model (Clustering + Classification)...")
        test_model()
        print("✅ Module Model OK!\n")
        
        print("🎯 3. Test du module Recommender (Similarité)...")
        test_recommender()
        print("✅ Module Recommender OK!\n")
        
        print("🚀 === PARTIE 2 COMPLÈTE ET FONCTIONNELLE ===")
        print("\nFichiers générés:")
        print("- data/models/vectorizer.pkl")
        print("- data/models/model.pkl") 
        print("- data/processed/features.npz")
        print("- data/processed/ml_results.json")
        print("- reports/recommendations_report.json")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# 🎬 Marketing AI - Agence Intelligence Cinéma

Projet d'analyse de données cinématographiques avec Machine Learning pour une agence marketing.

## 📋 Description

Outil intelligent qui collecte des données cinématographiques depuis plusieurs APIs, les analyse avec du machine learning et produit des visualisations et recommandations pour une agence marketing.

## 🎯 Objectifs

1. **Collecte** de données via APIs cinéma (TMDB, Reddit, OMDb)
2. **Nettoyage** et structuration des contenus textuels  
3. **Analyse ML** pour classifier et recommander des films
4. **Visualisations** et dashboard professionnel
5. **Rapport** synthétique avec métriques

## 🏗️ Architecture

```
marketing_ai/
├─ main.py                       # Orchestrateur principal
├─ core/                         # Modules métier
│  ├─ config.py                  # Configuration APIs & paramètres
│  ├─ fetcher.py                 # Collecte données APIs 
│  ├─ cleaner.py                 # Nettoyage NLP
│  ├─ analyzer.py                # Analyses descriptives
│  ├─ features.py                # Vectorisation TF-IDF
│  ├─ model.py                   # Machine Learning
│  ├─ recommender.py             # Système de recommandation
│  └─ viz.py                     # Visualisations & PDF
├─ data/
│  ├─ raw/                       # Données brutes APIs
│  ├─ processed/                 # Données nettoyées
│  └─ models/                    # Modèles ML (.pkl)
├─ reports/                      # Rapports JSON/CSV
├─ figs/                         # Visualisations PNG/SVG
└─ logs/                         # Journalisation
```

## 🚀 Installation

```bash
# Cloner le projet
git clone <repo-url>
cd marketing_ai

# Installer les dépendances
pip install -r requirements.txt

# Exécuter le pipeline complet
python main.py
```

## 🔧 Dépendances

- `pandas >= 1.5.0` - Manipulation de données
- `scikit-learn >= 1.2.0` - Machine Learning  
- `matplotlib >= 3.5.0` - Visualisations
- `requests >= 2.28.0` - Appels APIs
- `joblib >= 1.2.0` - Sauvegarde modèles

## 🎬 Sources de Données

### APIs Utilisées
1. **TMDB API** - Base de données films (synopsis, métadonnées)
2. **Reddit API** - Discussions communauté (/r/movies)  
3. **OMDb API** - Reviews et critiques détaillées

### Format des Données
```json
{
  "texts": ["texte film nettoyé...", "discussion reddit...", "review critique..."],
  "sources": ["tmdb", "reddit", "omdb"],
  "titles": ["Titre Film", "Discussion Title", "Review Title"]
}
```

## 🤖 Machine Learning

### Approche Choisie: Clustering Non-Supervisé
- **Algorithme**: K-Means (k=4-5 clusters)
- **Vectorisation**: TF-IDF (unigrams + bigrams)
- **Métriques**: Silhouette Score pour évaluation qualité

### Pipeline ML
1. **TF-IDF**: Transformation texte → vecteurs numériques (500 features max)
2. **Clustering**: Groupement automatique films par similarité
3. **Recommandation**: Similarité cosinus pour suggestions

### Résultats Attendus
- Clusters thématiques (sci-fi, action, horreur, comédie...)
- Score silhouette > 0.5 (objectif qualité)
- Système de recommandation top-k films similaires

## 📊 Visualisations

### 6 Figures Obligatoires
1. **sources_bar.png** - Volume par source de données
2. **top_keywords.png** - Mots-clés les plus fréquents
3. **latency_box.png** - Distribution latences APIs
4. **status_codes.png** - Répartition statuts HTTP
5. **timeline_activity.png** - Chronologie collecte
6. **ml_clusters.png** - Visualisation clusters ML

### Dashboard
- **dashboard.pdf** - Compilation toutes figures
- **summary.json** - KPIs consolidés  
- **keywords.csv** - Export mots-clés

## ⚙️ Configuration

### APIs & Tokens
```python
# core/config.py
APIS = {
    "tmdb": {
        "base_url": "https://api.themoviedb.org/3",
        "api_key": "YOUR_TMDB_KEY"
    },
    "reddit": {
        "base_url": "https://www.reddit.com",
        "user_agent": "MovieBot/1.0"
    },
    "omdb": {
        "base_url": "http://www.omdbapi.com",
        "api_key": "YOUR_OMDB_KEY" 
    }
}
```

### Paramètres ML
```python
RANDOM_STATE = 42          # Reproductibilité
TEST_SIZE = 0.3            # 70/30 train/test
MAX_FEATURES = 500         # TF-IDF features max
NGRAM_RANGE = (1, 2)       # Unigrammes + bigrammes
```

## 🧪 Tests

### Test Partie ML (Indépendant)
```bash
# Tester uniquement les modules ML avec données mock
python test_ml.py
```

### Test Modules Individuels  
```bash
# Tester chaque module séparément
python core/features.py
python core/model.py  
python core/recommender.py
```

## 📈 Métriques & Performance

### Clustering
- **Silhouette Score**: Mesure cohésion intra-cluster vs séparation inter-cluster
- **Objectif**: Score > 0.5 (qualité acceptable)
- **Interprétation**: Analyse top mots-clés par cluster

### Recommandation
- **Similarité Cosinus**: Mesure angle entre vecteurs TF-IDF
- **Top-K**: 3-5 films les plus similaires par requête
- **Validation**: Tests qualitatifs sur requêtes types

### APIs
- **Latence**: < 2s par appel (objectif performance)
- **Taux succès**: > 90% appels réussis  
- **Timeout**: 10s max par requête

## 🚧 Limitations & Améliorations

### Limitations Actuelles
- Pas de labels supervisés (clustering uniquement)
- Volume données limité (APIs gratuites)
- Pas de deep learning (contrainte projet)

### Améliorations Futures  
- Classification supervisée avec labels genres
- Analyse de sentiments sur reviews
- Intégration données temps réel
- Interface web interactive

## 👥 Équipe & Répartition

### Personne 1 - Data Pipeline
- `fetcher.py`, `cleaner.py`, `config.py`
- Collecte APIs + nettoyage NLP

### Personne 2 - Machine Learning  
- `features.py`, `model.py`, `recommender.py`
- TF-IDF + clustering + recommandation

### Personne 3 - Analytics & Viz
- `analyzer.py`, `viz.py`  
- KPIs + 6 visualisations + dashboard

## 📝 Reproduction

### Exécution Complète
```bash
python main.py
```

### Vérification Sorties
- ✅ `data/models/model.pkl` - Modèle ML sauvegardé
- ✅ `data/models/vectorizer.pkl` - Vectorizer TF-IDF
- ✅ `reports/summary.json` - KPIs consolidés
- ✅ `figs/*.png` - 6 visualisations
- ✅ `logs/marketing.log` - Logs détaillés

## 📞 Support

En cas de problème:
1. Vérifier les logs: `logs/marketing.log`
2. Tester modules individuellement  
3. Vérifier dépendances: `pip install -r requirements.txt`
4. Contacter l'équipe projet

---

## ⚠️ Note sur les clés API

Pour faciliter les tests, des données pré-collectées sont fournies dans `data/raw/`.
Si vous souhaitez re-collecter les données :
1. Créez un fichier `.env` à la racine
2. Ajoutez vos clés :
```
   TMDB_API_KEY=votre_clé_tmdb
   OMDB_API_KEY=votre_clé_omdb
```
3. Supprimez les fichiers dans `data/raw/`
4. Relancez `python main.py`

## 🤖 Résultats Machine Learning

### Clustering K-Means
- **Algorithme** : K-Means (k=3 clusters)
- **Métrique** : Silhouette Score = **0.0156**
- **Reproductibilité** : random_state=42 (fixé)

### Interprétation du score faible

Un silhouette score proche de 0 indique que les clusters sont **peu distincts**. 
Dans notre cas, cela s'explique par :

1. **Taille du dataset limitée** (50 documents)
   - K-Means nécessite ~500-1000 documents pour détecter des patterns robustes
   - Avec 16 documents par cluster en moyenne, la variance intra-cluster est élevée

2. **Hétérogénéité des sources**
   - Mélange de films (TMDb), critiques (OMDb) et séries (TVMaze)
   - 5 langues différentes (en, ja, no, fr, english)
   - Genres variés (action, comédie, drame, fantastique)
   
3. **Vocabulaire générique post-nettoyage**
   - Après suppression des stopwords, les textes courts perdent leur spécificité
   - Top mots-clés identiques entre clusters : "of", "his", "their"

### Validation qualitative

Malgré le score faible, l'analyse des clusters montre des **tendances thématiques** :

**Cluster 0** (15 docs) : Action et drames biographiques
- Exemples : *Jay Kelly*, *Dracula*, *Fight Club*
- Focus : personnages masculins en quête d'identité

**Cluster 1** (20 docs) : Films grand public et classiques
- Exemples : *Inception*, *The Godfather*, *Game of Thrones*
- Thèmes : histoires complexes, époques variées

**Cluster 2** (15 docs) : Femmes et familles
- Exemples : *Die My Love*, *Christy*, *Zootopia*
- Focus : protagonistes féminins, relations familiales

### Améliorations futures

Pour atteindre un score > 0.5 :
- Collecter 200+ documents via APIs
- Filtrer sur langue unique (EN uniquement)
- Tester k=2 clusters (simplification)
- Utiliser des embeddings (Word2Vec, BERT) au lieu de TF-IDF

### Système de recommandation
- **Méthode** : Similarité cosinus sur vecteurs TF-IDF
- **Top-K** : 3-5 films similaires par requête
- **Performance** : Scores entre 0.14 et 0.34 (acceptable pour un petit dataset)
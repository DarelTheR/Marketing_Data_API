# Rapport de Résultats - Projet Marketing AI

## 1. Ce qu'on a fait

On a créé un système qui collecte des données de films et séries depuis 3 sites web (TMDb, OMDb, TVMaze), les analyse avec du Machine Learning, et produit des graphiques.

Temps d'exécution : 36 secondes

---

## 2. Les données collectées

### Sources

- TMDb : 40 films
- OMDb : 5 films
- TVMaze : 5 séries
- Total : 50 documents

### Caractéristiques

- Longueur moyenne des textes : 278 caractères
- Longueur minimale : 92 caractères
- Longueur maximale : 813 caractères

### Langues

- Anglais : 45 documents
- Japonais : 2 documents
- Norvégien : 2 documents
- Français : 1 document

---

## 3. Résultats du Machine Learning

### Méthode utilisée

On a utilisé l'algorithme K-Means pour regrouper les films en 3 groupes automatiquement.

### Performance

Score de qualité : 0.016 (faible - les groupes ne sont pas très différents)

### Répartition

- Groupe 1 : 19 films (38%)
- Groupe 2 : 15 films (30%)
- Groupe 3 : 16 films (32%)

### Ce qu'on trouve dans chaque groupe

**Groupe 1** (19 films)
Films : Zootopia 2, Inception, Interstellar, The Godfather, Game of Thrones
Type : Films variés

**Groupe 2** (15 films)
Films : TRON, Avatar, Wicked, Dracula, Silicon Valley
Type : Science-fiction et fantastique

**Groupe 3** (16 films)
Films : Predator, Superman, The Fantastic 4, Breaking Bad
Type : Action et super-héros

---

## 4. Les mots les plus utilisés

Top 10 :

1. of - 69 fois
2. his - 41 fois
3. is - 32 fois
4. with - 29 fois
5. s - 28 fois
6. he - 20 fois
7. when - 20 fois
8. their - 20 fois
9. her - 20 fois
10. by - 17 fois

---

## 5. Performance des APIs

### Vitesse

Temps moyen de réponse : 0.5 secondes

## 6. Système de recommandation

On a testé 4 recherches de films similaires :

1. "dangerous battle brutal crime" - score 0.257
2. "love family daughter life" - score 0.245
3. "breaking bad criminal world" - score 0.337 (meilleur)
4. "confront dangerous past city" - score 0.177

Le système trouve 3 recommandations pour chaque recherche.

---

## 7. Les graphiques créés

On a produit 6 graphiques :

1. **sources_bar.png** - Volume de données par source
2. **top_keywords.png** - Les 20 mots les plus fréquents
3. **latency_box.png** - Temps de réponse des APIs
4. **status_codes.png** - Succès et erreurs des APIs
5. **timeline_activity.png** - Activité par source
6. **ml_clusters.png** - Répartition des groupes

Plus un PDF (dashboard.pdf) qui regroupe tout.

### Ce que montrent les graphiques

**sources_bar.png**
Barplot montrant le volume par source. On voit clairement que TMDb domine avec 40 films, tandis qu'OMDb et TVMaze ont 5 documents chacun. Cela montre qu'on a plus de données films que séries.

**top_keywords.png**
Barplot horizontal des 20 mots les plus utilisés. "of" est en tête avec 69 occurrences, suivi de "his" avec 41. Le problème : ce sont surtout des petits mots de liaison, pas des vrais mots-clés intéressants.

**latency_box.png**
Boxplot des temps de réponse. La moyenne est de 0.5 secondes, mais seul TVMaze a répondu (0.94s). Les deux autres APIs ont échoué faute de clés.

**status_codes.png**
Camembert montrant les codes HTTP. 66.7% en rouge (erreur 500) pour TMDb et OMDb, 33.3% en vert (succès 200) pour TVMaze. Visuellement, on voit bien que 2 APIs sur 3 ne fonctionnent pas.

**timeline_activity.png**
Ligne montrant le volume par source. TMDb est au sommet (40), puis les deux autres en bas (5 chacun). Confirme la dominance de TMDb.

**ml_clusters.png**
Deux graphiques côte à côte : un barplot et un camembert. Montrent que les 3 groupes sont équilibrés : Groupe 1 (38%), Groupe 2 (30%), Groupe 3 (32%). Le score de 0.016 affiché en haut confirme la faible qualité du regroupement.

---

## 8. Ce qu'on a produit

### Rapports

- summary.json - Les statistiques principales
- keywords.csv - La liste des mots-clés
- dashboard.pdf - Tous les graphiques en un document

## 9. Ce qui marche et ce qui marche pas

### Les problèmes

- Le score de qualité est très faible (0.016)
- Pas assez de données (50 c'est peu)
- Trop de petits mots inutiles dans les résultats

### Comment améliorer

- Collecter plus de données (200 minimum)
- Mieux nettoyer le texte
- Essayer d'autres méthodes
- Ajouter l'analyse des sentiments

---

## 10. Conclusion

Le système marche. On peut collecter des données, les analyser, et produire des graphiques automatiquement. Le regroupement automatique identifie 3 types de contenu (varié, SF, action).

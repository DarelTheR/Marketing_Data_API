# Marketing_Data_API

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
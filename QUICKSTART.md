# Guide de Démarrage Rapide

## 🚀 Installation et Configuration

```bash
# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Configuration de la clé API
cp .env.example .env
# Éditez .env et ajoutez votre clé NewsAPI

# 3. Test rapide
python exemple_pipeline.py --query "test" --max-results 5
```

## 📋 Utilisation Standard

### Option 1: Pipeline Automatique (Recommandé)
```bash
# Exécution complète avec paramètres par défaut
python exemple_pipeline.py

# Avec paramètres personnalisés
python exemple_pipeline.py --query "machine learning" --days 14 --max-results 20
```

### Option 2: Exécution Manuelle Étape par Étape
```bash
# Étape 1: Collecte
python 1_search_tools.py "intelligence artificielle" --from-date 2025-07-01 --max-results 10

# Étape 2: Analyse de sentiment
python 2_analyse_sentiments.py

# Étape 3: Traduction
python 3_traduction.py

# Étape 4: Rapport
python 4_analyse_fichier.py resultats_sentiments_corpus_traduit.json
```

## 📊 Fichiers de Sortie

| Fichier | Description | Usage |
|---------|-------------|-------|
| `resultats_news*.txt` | Articles bruts par langue | Lecture humaine |
| `corpus_concatene.txt` | Tous les titres | Vérification |
| `resultats_sentiments_corpus.json` | Analyse de sentiment | Données structurées |
| `resultats_sentiments_corpus_traduit.json` | Avec traductions | Analyse finale |

## ⚠️ Résolution de Problèmes

### Erreurs Fréquentes
- **"NEWSAPI_KEY manquante"** → Vérifiez votre fichier `.env`
- **"Aucun fichier trouvé"** → Exécutez d'abord l'étape de collecte
- **Modèles lents à charger** → Normal au premier usage (téléchargement)

### Performance
- Premier lancement : 5-10 minutes (téléchargement des modèles)
- Lancements suivants : 1-2 minutes pour 10 articles
- Espace disque requis : ~3-5 GB (modèles NLP)

## 📝 Personnalisation

### Changer la Langue de Collecte
```python
# Dans 1_search_tools.py, ligne ~35
f'language=fr&'  # Remplacer 'zh' par 'fr', 'en', etc.
```

### Ajouter une Nouvelle Langue de Traduction
```python
# Dans 3_traduction.py, ajouter à lang2model:
'ja': 'Helsinki-NLP/opus-mt-ja-fr',  # Japonais vers français
```

## 🎯 Cas d'Usage Typiques

- **Veille technologique** : Sentiment sur "IA", "blockchain", etc.
- **Analyse de marque** : Perception d'une entreprise dans l'actualité
- **Recherche académique** : Évolution du sentiment sur un sujet
- **Journalisme** : Tendances dans le traitement médiatique

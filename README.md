# 📰 Analyseur de Sentiment d'Actualités Multilingue

> **Pipeline d'analyse de sentiment automatisé pour articles d'actualité en plusieurs langues**

Ce projet implémente un pipeline complet d'analyse de sentiment pour des articles d'actualité récupérés via l'API NewsAPI. Il permet de collecter, analyser et interpréter le sentiment de titres d'articles dans différentes langues avec traduction automatique vers le français.

## 🎯 Objectifs du Projet

- **Collecte automatisée** d'actualités via l'API NewsAPI
- **Analyse de sentiment** multilingue avec des modèles de NLP pré-entraînés
- **Traduction automatique** vers le français pour une analyse unifiée
- **Génération de rapports** détaillés avec statistiques et recommandations

## 📋 Table des Matières

1. [Architecture du Projet](#-architecture-du-projet)
2. [Installation](#-installation)
3. [Configuration](#-configuration)
4. [Guide d'Utilisation](#-guide-dutilisation)
5. [Modules Détaillés](#-modules-détaillés)
6. [Format des Données](#-format-des-données)
7. [Exemples de Résultats](#-exemples-de-résultats)
8. [Limitations et Biais](#-limitations-et-biais)
9. [Contribuer](#-contribuer)

## 🏗️ Architecture du Projet

Le projet est organisé en 4 modules séquentiels qui forment un pipeline de traitement :

```
📦 News_api/
├── 1_search_tools.py          # 🔍 Collecte d'actualités
├── 2_analyse_sentiments.py    # 🎭 Analyse de sentiment
├── 3_traduction.py            # 🌍 Traduction automatique
├── 4_analyse_fichier.py       # 📊 Génération de rapports
├── resultats_news_*.txt       # 📄 Articles par langue
├── corpus_concatene.txt       # 📄 Tous les titres
├── resultats_sentiments_corpus.json         # 📄 Résultats d'analyse
├── resultats_sentiments_corpus_traduit.json # 📄 Avec traductions
└── README.md                  # 📖 Documentation
```

### Flux de Données

```mermaid
graph LR
    A[NewsAPI] --> B[1_search_tools.py]
    B --> C[resultats_news_*.txt]
    C --> D[2_analyse_sentiments.py]
    D --> E[resultats_sentiments_corpus.json]
    E --> F[3_traduction.py]
    F --> G[resultats_sentiments_corpus_traduit.json]
    G --> H[4_analyse_fichier.py]
    H --> I[Rapport d'Analyse]
```

## 🚀 Installation

### Prérequis

- **Python 3.8+**
- **Clé API NewsAPI** (gratuite sur [newsapi.org](https://newsapi.org))

### Installation des Dépendances

```bash
# Clonage du projet
git clone <url-du-projet>
cd News_api

# Installation des dépendances Python
pip install -r requirements.txt

# Si requirements.txt n'existe pas, installer manuellement :
pip install requests python-dotenv transformers torch tqdm
```

### Dépendances Principales

| Package | Version | Usage |
|---------|---------|-------|
| `requests` | >= 2.25.0 | Requêtes HTTP vers NewsAPI |
| `python-dotenv` | >= 0.19.0 | Gestion des variables d'environnement |
| `transformers` | >= 4.20.0 | Modèles de NLP (sentiment + traduction) |
| `torch` | >= 1.12.0 | Framework d'inférence PyTorch |
| `tqdm` | >= 4.60.0 | Barres de progression |

## ⚙️ Configuration

### 1. Configuration de l'API NewsAPI

Créez un fichier `.env` à la racine du projet :

```bash
# .env
NEWSAPI_KEY=votre_cle_api_newsapi_ici
```

Pour obtenir une clé API :
1. Visitez [newsapi.org](https://newsapi.org)
2. Créez un compte gratuit
3. Copiez votre clé API dans le fichier `.env`

### 2. Configuration des Langues (Optionnel)

Par défaut, le système supporte 13 langues. Pour ajouter d'autres langues, modifiez le dictionnaire `lang2model` dans `3_traduction.py` :

```python
lang2model = {
    'votre_langue': 'Helsinki-NLP/opus-mt-votre_langue-fr',
    # ...
}
```

## 📖 Guide d'Utilisation

### Exécution Complète du Pipeline

```bash
# 1. Collecte d'actualités (exemple avec "intelligence artificielle")
python 1_search_tools.py "intelligence artificielle" --from-date 2025-07-01 --max-results 10

# 2. Analyse de sentiment (traite tous les fichiers resultats_news_*.txt)
python 2_analyse_sentiments.py

# 3. Traduction automatique vers le français
python 3_traduction.py

# 4. Génération du rapport d'analyse
python 4_analyse_fichier.py resultats_sentiments_corpus_traduit.json
```

### Options Avancées de Recherche

```bash
# Recherche avec paramètres personnalisés
python 1_search_tools.py "machine learning" \
    --from-date 2025-06-01 \
    --sort popularity \
    --max-results 20

# Paramètres disponibles :
# --from-date : Date de début (YYYY-MM-DD)
# --sort : relevancy | popularity | publishedAt
# --max-results : Nombre d'articles (1-100)
```

### Analyse de Fichiers Spécifiques

```bash
# Analyse d'un fichier de résultats spécifique
python 4_analyse_fichier.py resultats_sentiments_corpus.json
```

## 📚 Modules Détaillés

### 🔍 Module 1: Collecte d'Actualités (`1_search_tools.py`)

**Rôle** : Récupération d'articles via l'API NewsAPI

**Fonctionnalités** :
- Recherche par mots-clés avec filtres temporels
- Support de différentes langues et critères de tri
- Formatage structuré des résultats (titre, source, date, description, URL)
- Sauvegarde automatique en fichiers texte

**Configuration dans le code** :
```python
# Langue actuellement fixée en chinois (zh)
# Pour changer : modifier la ligne dans format_news_context()
f'language=fr&'  # Exemple pour le français
```

**Formats de sortie** :
- `resultats_news.txt` : Articles formatés
- Structure : `- Titre (Source, Date) — Description\n  URL`

### 🎭 Module 2: Analyse de Sentiment (`2_analyse_sentiments.py`)

**Rôle** : Classification automatique du sentiment des titres

**Modèle utilisé** :
- `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- Modèle multilingue pré-entraîné sur Twitter
- Classifications : positif, neutre, négatif

**Processus** :
1. Scan automatique des fichiers `resultats_news_*.txt`
2. Extraction des codes de langue depuis les noms de fichiers
3. Analyse de sentiment avec scores de confiance
4. Génération de statistiques globales

**Sortie** :
- `corpus_concatene.txt` : Tous les titres extraits
- `resultats_sentiments_corpus.json` : Résultats détaillés

### 🌍 Module 3: Traduction Automatique (`3_traduction.py`)

**Rôle** : Traduction des titres non-français vers le français

**Modèles utilisés** :
- Série `Helsinki-NLP/opus-mt-*-fr` (MarianMT)
- Support de 12 langues : en, de, es, it, nl, pt, ru, zh, ar, he, no, sv

**Optimisations** :
- Chargement paresseux des modèles (une fois par langue)
- Cache des modèles en mémoire
- Gestion d'erreurs robuste

**Sortie** :
- `resultats_sentiments_corpus_traduit.json` : Données enrichies avec traductions

### 📊 Module 4: Analyse et Rapports (`4_analyse_fichier.py`)

**Rôle** : Génération de rapports détaillés et recommandations

**Sections du rapport** :
1. **Statistiques générales** : Répartition des sentiments avec pourcentages
2. **Analyse de tendance** : Sentiment dominant et interprétation
3. **Exemples représentatifs** : Meilleurs exemples par sentiment (score le plus élevé)
4. **Analyse qualitative** : Recommandations d'interprétation et limitations

**Fonctionnalités avancées** :
- Tri des exemples par score de confiance
- Recommandations contextuelles basées sur la répartition
- Alertes sur les biais méthodologiques

## 📄 Format des Données

### Structure des Fichiers JSON

#### `resultats_sentiments_corpus.json`
```json
[
  {
    "langue": "fr",
    "titre": "L'IA révolutionne l'industrie pharmaceutique",
    "sentiment": "positif", 
    "score": 0.8945
  }
]
```

#### `resultats_sentiments_corpus_traduit.json`
```json
[
  {
    "langue": "en",
    "titre": "AI transforms healthcare industry",
    "sentiment": "positif",
    "score": 0.8234,
    "traduction": "L'IA transforme l'industrie de la santé"
  }
]
```

### Codes de Langues Supportés

| Code | Langue | Modèle de Traduction |
|------|--------|---------------------|
| `fr` | Français | (pas de traduction) |
| `en` | Anglais | opus-mt-en-fr |
| `de` | Allemand | opus-mt-de-fr |
| `es` | Espagnol | opus-mt-es-fr |
| `it` | Italien | opus-mt-it-fr |
| `nl` | Néerlandais | opus-mt-nl-fr |
| `pt` | Portugais | opus-mt-pt-fr |
| `ru` | Russe | opus-mt-ru-fr |
| `zh` | Chinois | opus-mt-zh-fr |
| `ar` | Arabe | opus-mt-ar-fr |
| `he` | Hébreu | opus-mt-he-fr |
| `no` | Norvégien | opus-mt-no-fr |
| `sv` | Suédois | opus-mt-sv-fr |

## 📈 Exemples de Résultats

### Rapport d'Analyse Type

```
============================================================
RAPPORT D'ANALYSE DE SENTIMENT
============================================================
Fichier analysé: resultats_sentiments_corpus_traduit.json
Nombre total de titres analysés: 150

Répartition des sentiments:
    Positif :   65 articles ( 43.3%)
    Neutre  :   52 articles ( 34.7%)
    Négatif :   33 articles ( 22.0%)

========================================
ANALYSE DE TENDANCE  
========================================
Sentiment dominant: 'positif' (43.3% des articles)
→ Tendance MODÉRÉE vers le sentiment positif

========================================
EXEMPLES REPRÉSENTATIFS
========================================

--- SENTIMENT POSITIF ---
Titre original: Revolutionary AI breakthrough in medical diagnosis
Score de confiance: 0.924
Traduction FR: Percée révolutionnaire de l'IA dans le diagnostic médical
Langue source: en

--- SENTIMENT NÉGATIF ---
Titre original: AI threatens millions of jobs, experts warn
Score de confiance: 0.887
Traduction FR: L'IA menace des millions d'emplois, avertissent les experts
Langue source: en

========================================
ANALYSE QUALITATIVE
========================================

Recommandations d'interprétation:
→ Couverture médiatique ÉQUILIBRÉE
  Approche nuancée du sujet, aspects positifs et négatifs

Limitations à considérer:
• Biais possible selon la nature du corpus (sources, période, géographie)
• Modèle d'IA: classifications automatiques à vérifier manuellement
• Titres 'clickbait' peuvent fausser l'analyse de sentiment
• Différences culturelles dans l'expression des sentiments
```

## ⚠️ Limitations et Biais

### Limitations Techniques

1. **Qualité de la traduction** : Les modèles Helsinki-NLP peuvent avoir des erreurs sur des textes techniques ou des expressions idiomatiques
2. **Classification de sentiment** : Le modèle est entraîné sur Twitter, peut ne pas capturer toutes les nuances journalistiques
3. **Langue fixe dans la collecte** : Actuellement configuré pour le chinois dans `1_search_tools.py`

### Biais Méthodologiques

1. **Biais de source** : NewsAPI privilégie certaines sources selon la région
2. **Biais temporel** : L'analyse reflète l'actualité d'une période donnée
3. **Biais linguistique** : Différences culturelles dans l'expression des sentiments
4. **Biais algorithmique** : Les modèles peuvent avoir des préjugés intégrés

### Recommandations d'Usage

- ✅ **Analyser les tendances générales** plutôt que des articles individuels
- ✅ **Comparer plusieurs périodes** pour identifier des évolutions
- ✅ **Vérifier manuellement** les classifications sur des échantillons
- ❌ **Ne pas utiliser** pour des décisions critiques sans validation humaine

## 🔧 Personnalisation

### Ajout de Nouvelles Langues

1. Vérifiez la disponibilité d'un modèle Helsinki-NLP : `opus-mt-{langue}-fr`
2. Ajoutez l'entrée dans `lang2model` dans `3_traduction.py`
3. Testez avec quelques exemples

### Modification des Modèles

#### Changement du Modèle de Sentiment
```python
# Dans 2_analyse_sentiments.py
MODEL = "nouveau_modele_sentiment"  # Ex: "nlptown/bert-base-multilingual-uncased-sentiment"
id2label = {0: "négatif", 1: "positif"}  # Adapter selon le modèle
```

#### Utilisation d'Autres APIs d'Actualités
```python
# Dans 1_search_tools.py - remplacer la fonction format_news_context()
def format_news_context_custom(query, **params):
    # Implémentation pour autre API (ex: Guardian, NY Times)
    pass
```

## 🐛 Dépannage

### Problèmes Fréquents

#### Erreur "NEWSAPI_KEY manquante"
```bash
# Solution : Vérifiez votre fichier .env
echo "NEWSAPI_KEY=votre_cle_ici" > .env
```

#### Erreur de téléchargement de modèles
```bash
# Les modèles Transformers sont volumineux (500MB-2GB chacun)
# Assurez-vous d'avoir suffisamment d'espace disque et une connexion stable
```

#### Performances lentes
```python
# Réduisez le nombre d'articles ou utilisez un GPU
python 1_search_tools.py "query" --max-results 5  # Au lieu de 50
```

### Messages d'Erreur et Solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ModuleNotFoundError: transformers` | Dépendance manquante | `pip install transformers torch` |
| `HTTP 401 NewsAPI` | Clé API invalide | Vérifier la clé dans `.env` |
| `No such file: resultats_news*.txt` | Pas de fichiers d'entrée | Exécuter d'abord `1_search_tools.py` |
| `CUDA out of memory` | Modèle trop grand pour GPU | Forcer l'usage CPU : `export CUDA_VISIBLE_DEVICES=""` |

## 🤝 Contribuer

### Structure de Contribution

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Committez** vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Pushez** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créez** une Pull Request

### Améliorations Bienvenues

- 🌐 **Support de nouvelles langues** et APIs d'actualités
- 📊 **Visualisations** avec matplotlib/plotly
- 🔍 **Analyse plus fine** par source, région, ou catégorie
- ⚡ **Optimisations de performance** (parallélisation, cache)
- 🧪 **Tests unitaires** et intégration continue
- 📱 **Interface web** avec Flask/FastAPI

### Standards de Code

- **Documentation** : Docstrings Python détaillées
- **Style** : Respect de PEP 8
- **Tests** : Coverage minimale de 80%
- **Sécurité** : Pas de clés API dans le code

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues GitHub** : Pour les bugs et demandes de fonctionnalités
- **Discussions** : Pour les questions générales et l'aide à l'usage
- **Documentation** : Ce README et les commentaires dans le code

---

**Version** : 1.0.0  
**Dernière mise à jour** : Juillet 2025  
**Auteur** : [Votre nom]  
**Statut** : Production Ready ✅

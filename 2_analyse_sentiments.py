"""
Module d'analyse de sentiment des actualités.

Ce module traite les fichiers d'actualités générés par 1_search_tools.py
pour effectuer une analyse de sentiment sur les titres d'articles.
Il utilise un modèle de transformeur pré-entraîné pour classifier 
les sentiments en positif, neutre ou négatif.

Dépendances:
- transformers: bibliothèque HuggingFace pour les modèles de NLP
- torch: framework PyTorch pour l'inférence du modèle
- tqdm: barre de progression pour le traitement en lot
- glob: recherche de fichiers par motif

Modèle utilisé:
- cardiffnlp/twitter-xlm-roberta-base-sentiment: modèle multilingue 
  pré-entraîné sur Twitter pour l'analyse de sentiment
"""

import os
from glob import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
from tqdm import tqdm
import re

# 1. Recherche automatique de tous les fichiers de résultats d'actualités
# Pattern: resultats_news*.txt (ex: resultats_news_fr.txt, resultats_news_en.txt)
fichiers = sorted(glob("resultats_news*.txt"))

if not fichiers:
    print("Aucun fichier trouvé. Veuillez d'abord exécuter 1_search_tools.py")
    exit(1)

print(f"Fichiers trouvés: {fichiers}")

# 2. Extraction et concaténation des titres de tous les fichiers
# Conservation de l'information de langue pour chaque titre
all_titles = []
for fichier in fichiers:
    # Extraction du code langue depuis le nom de fichier (ex: resultats_news_fr.txt -> fr)
    m = re.search(r'resultats_news_([a-z]{2})\.txt', os.path.basename(fichier))
    langue = m.group(1) if m else "??"  # Code langue ou ?? si non trouvé
    
    with open(fichier, "r", encoding="utf-8") as f:
        for line in f:
            l = line.strip()
            # Filtrage: on ne prend que les lignes de titre (commencent par '- ')
            # et on évite les URLs (qui ne commencent pas par 'http')
            if l.startswith("- ") and not l.startswith("http"):
                titre = l[2:].strip()  # Suppression du préfixe '- '
                all_titles.append({"langue": langue, "titre": titre})

# Sauvegarde optionnelle du corpus concaténé pour inspection
with open("corpus_concatene.txt", "w", encoding="utf-8") as out:
    for entry in all_titles:
        out.write(entry["titre"] + "\n")

print(f"{len(all_titles)} titres extraits et concaténés dans corpus_concatene.txt")

# 3. Configuration du modèle d'analyse de sentiment
# Utilisation d'un modèle multilingue pré-entraîné de Cardiff NLP
MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
print(f"Chargement du modèle de sentiment: {MODEL}")

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Mapping des IDs de labels vers des noms compréhensibles
id2label = {0: "négatif", 1: "neutre", 2: "positif"}

def analyze_sentiment(text):
    """
    Analyse le sentiment d'un texte donné.
    
    Args:
        text (str): Texte à analyser
        
    Returns:
        tuple: (label_sentiment, score_confiance)
            - label_sentiment (str): "positif", "neutre" ou "négatif"
            - score_confiance (float): Score de confiance entre 0 et 1
    """
    # Tokenisation du texte avec troncature si nécessaire
    tokens = tokenizer(text, return_tensors='pt', truncation=True)
    
    # Inférence sans calcul de gradients (plus rapide)
    with torch.no_grad():
        outputs = model(**tokens)
        # Application de softmax pour obtenir des probabilités
        scores = outputs.logits.softmax(dim=1).squeeze()
        # Sélection du label avec la probabilité la plus élevée
        label_id = int(scores.argmax())
    
    return id2label[label_id], float(scores[label_id])

# 4. Traitement en lot de tous les titres
print("Analyse de sentiment en cours...")
results = []

for entry in tqdm(all_titles, desc="Analyse de sentiment"):
    sentiment, score = analyze_sentiment(entry["titre"])
    results.append({
        "langue": entry["langue"],
        "titre": entry["titre"],
        "sentiment": sentiment,
        "score": score
    })

# 5. Génération de statistiques globales
# Comptage des sentiments toutes langues confondues
counts = {"positif": 0, "neutre": 0, "négatif": 0}
for r in results:
    counts[r["sentiment"]] += 1

print("\n--- Résumé global de l'analyse de sentiment ---")
total_articles = len(results)
print(f"Total d'articles analysés: {total_articles}")
print(f"Positifs : {counts['positif']} ({counts['positif']/total_articles*100:.1f}%)")
print(f"Neutres  : {counts['neutre']} ({counts['neutre']/total_articles*100:.1f}%)")
print(f"Négatifs : {counts['négatif']} ({counts['négatif']/total_articles*100:.1f}%)")

# 6. Sauvegarde des résultats détaillés en JSON
output_file = "resultats_sentiments_corpus.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nLes résultats détaillés ont été enregistrés dans {output_file}")
print("Ce fichier contient pour chaque titre: langue, texte, sentiment et score de confiance")
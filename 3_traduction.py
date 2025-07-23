"""
Module de traduction automatique pour l'analyse multilingue.

Ce module traduit automatiquement les titres d'actualités non-français
vers le français en utilisant les modèles de traduction Helsinki-NLP.
Il traite le fichier JSON généré par l'analyse de sentiment et ajoute
une colonne 'traduction' pour faciliter l'analyse en français.

Dépendances:
- transformers: pour les modèles de traduction MarianMT
- tqdm: barre de progression pour le traitement

Modèles utilisés:
- Série Helsinki-NLP/opus-mt-*-fr: modèles de traduction vers le français
  pour différentes langues sources (en, de, es, it, nl, pt, ru, zh, ar, he, no, sv)
"""

import json
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

# Chargement du fichier d'analyse de sentiment
print("Chargement du fichier d'analyse de sentiment...")
with open("resultats_sentiments_corpus.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Fichier chargé: {len(data)} entrées trouvées")

# Dictionnaire de mapping: code langue -> modèle de traduction Helsinki-NLP
# Tous les modèles traduisent vers le français (suffixe -fr)
lang2model = {
    'en': 'Helsinki-NLP/opus-mt-en-fr',    # Anglais -> Français
    'de': 'Helsinki-NLP/opus-mt-de-fr',    # Allemand -> Français  
    'es': 'Helsinki-NLP/opus-mt-es-fr',    # Espagnol -> Français
    'it': 'Helsinki-NLP/opus-mt-it-fr',    # Italien -> Français
    'nl': 'Helsinki-NLP/opus-mt-nl-fr',    # Néerlandais -> Français
    'pt': 'Helsinki-NLP/opus-mt-pt-fr',    # Portugais -> Français
    'ru': 'Helsinki-NLP/opus-mt-ru-fr',    # Russe -> Français
    'zh': 'Helsinki-NLP/opus-mt-zh-fr',    # Chinois -> Français
    'ar': 'Helsinki-NLP/opus-mt-ar-fr',    # Arabe -> Français
    'he': 'Helsinki-NLP/opus-mt-he-fr',    # Hébreu -> Français
    'no': 'Helsinki-NLP/opus-mt-no-fr',    # Norvégien -> Français
    'sv': 'Helsinki-NLP/opus-mt-sv-fr',    # Suédois -> Français
    # Ajouter d'autres langues au besoin en respectant le format opus-mt-XX-fr
}

# Cache pour éviter de recharger les modèles à chaque traduction
# Structure: {nom_modèle: (tokenizer, model)}
loaded_models = {}

def translate(text, lang):
    """
    Traduit un texte vers le français selon la langue source.
    
    Args:
        text (str): Texte à traduire
        lang (str): Code de langue source (ex: 'en', 'de', 'es')
        
    Returns:
        str: Texte traduit en français, ou texte original si langue=fr,
             ou chaîne vide si langue non supportée ou erreur
    """
    # Pas de traduction nécessaire si déjà en français
    if lang == 'fr':
        return text
    
    # Vérification de la disponibilité du modèle pour cette langue
    if lang not in lang2model:
        print(f"Langue '{lang}' non supportée pour la traduction")
        return ""
    
    model_name = lang2model[lang]
    
    # Chargement paresseux du modèle (une seule fois par modèle)
    if model_name not in loaded_models:
        print(f"Chargement du modèle de traduction: {model_name}")
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            loaded_models[model_name] = (tokenizer, model)
        except Exception as e:
            print(f"Erreur lors du chargement du modèle {model_name}: {e}")
            return ""
    
    tokenizer, model = loaded_models[model_name]
    
    # Exécution de la traduction
    try:
        # Préparation du batch pour la traduction sequence-to-sequence
        batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
        # Génération de la traduction
        gen = model.generate(**batch)
        # Décodage du résultat en supprimant les tokens spéciaux
        return tokenizer.decode(gen[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Erreur lors de la traduction de '{text[:50]}...': {e}")
        return ""

# Traitement de toutes les entrées pour ajouter les traductions
print("Début de la traduction automatique...")

# Comptage des langues pour information
langues_detectees = {}
for entry in data:
    lang = entry.get('langue', '')
    langues_detectees[lang] = langues_detectees.get(lang, 0) + 1

print(f"Langues détectées: {langues_detectees}")

# Application de la traduction avec barre de progression
for entry in tqdm(data, desc="Traduction en cours"):
    lang = entry.get('langue', '')
    titre = entry.get('titre', '')
    
    # On ne retraduit pas si déjà en français ou si une traduction existe déjà
    if lang != 'fr' and not entry.get('traduction'):
        try:
            traduction = translate(titre, lang)
            entry['traduction'] = traduction
            
            # Log des échecs de traduction pour debug
            if not traduction:
                print(f"Échec traduction pour {lang}: {titre[:50]}...")
                
        except Exception as e:
            entry['traduction'] = ""
            print(f"Erreur traduction {lang} - {titre[:30]}...: {e}")

# Sauvegarde du fichier enrichi avec les traductions
output_file = "resultats_sentiments_corpus_traduit.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTraduction terminée!")
print(f"Nouveau fichier avec traductions généré: {output_file}")
print("Structure enrichie: langue, titre, sentiment, score, traduction (si applicable)")
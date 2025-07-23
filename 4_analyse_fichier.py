"""
Module d'analyse et de rapport des résultats de sentiment.

Ce module fournit des outils d'analyse et de visualisation des résultats
d'analyse de sentiment. Il génère des rapports détaillés avec statistiques,
exemples représentatifs et recommandations d'interprétation.

Fonctionnalités:
- Statistiques globales de répartition des sentiments
- Exemples représentatifs pour chaque catégorie de sentiment  
- Analyse de tendances et recommandations d'interprétation
- Support des fichiers avec et sans traductions

Usage:
    python 4_analyse_fichier.py resultats_sentiments_corpus_traduit.json
"""

import json
from collections import Counter

def analyser_fichier_sentiments(nom_fichier):
    """
    Analyse un fichier JSON de résultats de sentiment et génère un rapport complet.
    
    Args:
        nom_fichier (str): Chemin vers le fichier JSON contenant les résultats
                          de l'analyse de sentiment
    
    Le fichier JSON doit contenir une liste d'objets avec les clés:
    - 'sentiment': classification du sentiment ('positif', 'neutre', 'négatif')
    - 'titre': titre original de l'article
    - 'score': score de confiance de la classification
    - 'traduction': traduction française (optionnel)
    - 'langue': code de langue source (optionnel)
    """
    # Chargement et validation du fichier
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {nom_fichier} n'existe pas.")
        return
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier {nom_fichier} n'est pas un JSON valide.")
        return

    if not isinstance(data, list):
        print("Erreur: Le fichier doit contenir une liste d'objets JSON.")
        return

    # Extraction des données avec gestion de compatibilité
    # (anciens fichiers peuvent avoir 'sentiments' au lieu de 'sentiment')
    sentiments = [item.get('sentiment', '') for item in data if 'sentiment' in item and item['sentiment']]
    titres = [item.get('titre', '') for item in data]
    total = len(sentiments)
    repartition = Counter(sentiments)

    # === SECTION 1: STATISTIQUES GÉNÉRALES ===
    print(f"\n{'='*60}")
    print(f"RAPPORT D'ANALYSE DE SENTIMENT")
    print(f"{'='*60}")
    print(f"Fichier analysé: {nom_fichier}")
    print(f"Nombre total de titres analysés: {total}")
    
    if total == 0:
        print("Aucun titre avec sentiment détecté dans le fichier.")
        return
    
    print(f"\nRépartition des sentiments:")
    for sentiment, count in repartition.items():
        pourcentage = (count / total) * 100
        print(f"  {sentiment.capitalize():>8} : {count:>4} articles ({pourcentage:>5.1f}%)")

    # === SECTION 2: TENDANCE DOMINANTE ===
    print(f"\n{'='*40}")
    print("ANALYSE DE TENDANCE")
    print(f"{'='*40}")
    
    if repartition:
        dominant = repartition.most_common(1)[0][0]
        dominant_count = repartition.most_common(1)[0][1]
        dominant_pct = (dominant_count / total) * 100
        
        print(f"Sentiment dominant: '{dominant}' ({dominant_pct:.1f}% des articles)")
        
        # Interprétation de la tendance
        if dominant_pct > 50:
            print(f"→ Tendance FORTE vers le sentiment {dominant}")
        elif dominant_pct > 40:
            print(f"→ Tendance MODÉRÉE vers le sentiment {dominant}")
        else:
            print(f"→ Répartition ÉQUILIBRÉE, légère tendance {dominant}")
    else:
        print("Aucune tendance détectée (données insuffisantes).")

    # === SECTION 3: EXEMPLES REPRÉSENTATIFS ===
    print(f"\n{'='*50}")
    print("EXEMPLES REPRÉSENTATIFS PAR SENTIMENT")
    print(f"{'='*50}")
    
    # Affichage d'exemples pour chaque sentiment avec scores de confiance
    for sentiment in ['positif', 'neutre', 'négatif']:
        exemples = [item for item in data if item.get('sentiment') == sentiment]
        if exemples:
            # Tri par score de confiance décroissant pour prendre le meilleur exemple
            exemples_tries = sorted(exemples, key=lambda x: x.get('score', 0), reverse=True)
            exemple = exemples_tries[0]  # Exemple avec le score le plus élevé
            
            print(f"\n--- SENTIMENT {sentiment.upper()} ---")
            print(f"Titre original: {exemple.get('titre','')}")
            print(f"Score de confiance: {exemple.get('score', 0):.3f}")
            
            # Affichage des informations supplémentaires si disponibles
            traduction = exemple.get('traduction', '')
            if traduction and traduction.strip():
                print(f"Traduction FR: {traduction}")
            
            langue = exemple.get('langue', '')
            if langue:
                print(f"Langue source: {langue}")

    # === SECTION 4: ANALYSE QUALITATIVE ET RECOMMANDATIONS ===
    print(f"\n{'='*50}")
    print("ANALYSE QUALITATIVE ET RECOMMANDATIONS")
    print(f"{'='*50}")
    
    print("\nObservations méthodologiques:")
    print("• Les titres promotionnels ou porteurs d'innovation tendent vers le POSITIF")
    print("• Les titres à tonalité problématique ou polémique sont généralement NÉGATIFS") 
    print("• Les titres purement informatifs/factuels sont classés NEUTRES")
    print("• Les titres interrogatifs peuvent être sur-classés en neutre")

    print(f"\nRecommandations d'interprétation:")
    
    # Génération de recommandations contextuelles basées sur la répartition
    positif_count = repartition.get('positif', 0)
    negatif_count = repartition.get('négatif', 0)
    
    if positif_count > negatif_count * 1.5:
        print("→ Couverture médiatique majoritairement OPTIMISTE")
        print("  Le sujet est perçu positivement, innovation mise en avant")
    elif negatif_count > positif_count * 1.5:
        print("→ Couverture médiatique majoritairement CRITIQUE")
        print("  Préoccupations, risques ou controverses dominants")
    else:
        print("→ Couverture médiatique ÉQUILIBRÉE")
        print("  Approche nuancée du sujet, aspects positifs et négatifs")

    print(f"\nLimitations importantes à considérer:")
    print("• Biais possible selon la nature du corpus (sources, période, géographie)")
    print("• Modèle d'IA: classifications automatiques à vérifier manuellement") 
    print("• Titres 'clickbait' peuvent fausser l'analyse de sentiment")
    print("• Différences culturelles dans l'expression des sentiments")
    print("• Modèle entraîné sur Twitter: peut ne pas capturer toutes les nuances journalistiques")

    # Exemples
    print("\nExemples :")
    for sentiment in ['positif', 'neutre', 'négatif']:
        exemples = [item for item in data if item.get('sentiment') == sentiment]
        if exemples:
            exemple = exemples[0]
            print(f"\n{sentiment.capitalize()} :")
            print(f"  Titre : {exemple.get('titre','')}")
            print(f"  Score : {exemple.get('score','')}")
            traduction = exemple.get('traduction', '')
            if traduction:
                print(f"  Traduction : {traduction}")

    # Synthèse rapide
    print("\nSynthèse critique :")
    print("- Les titres promotionnels ou porteurs d’innovation sont souvent positifs.")
    print("- Les titres à tonalité problématique ou polémique sont généralement négatifs.")
    print("- Les titres purement informatifs sont classés neutres.")
    print("- Vérifier manuellement les titres 'question' ou 'alerte', ils peuvent être surclassés en neutre ou positif.")
    print("- Biais possible selon la nature du corpus (tech, presse, question, polémique).")

if __name__ == "__main__":
    """
    Point d'entrée du script pour l'analyse en ligne de commande.
    
    Usage: python 4_analyse_fichier.py fichier.json
    
    Exemple:
        python 4_analyse_fichier.py resultats_sentiments_corpus_traduit.json
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: python 4_analyse_fichier.py <fichier_json>")
        print("Exemple: python 4_analyse_fichier.py resultats_sentiments_corpus_traduit.json")
        exit(1)
    
    # Lancement de l'analyse avec le fichier fourni en argument
    analyser_fichier_sentiments(sys.argv[1])
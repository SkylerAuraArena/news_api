#!/usr/bin/env python3
"""
Script d'exemple pour démontrer l'utilisation complète du pipeline
d'analyse de sentiment d'actualités multilingue.

Ce script exécute automatiquement toutes les étapes du pipeline :
1. Collecte d'actualités via NewsAPI
2. Analyse de sentiment multilingue  
3. Traduction automatique vers le français
4. Génération de rapport d'analyse

Usage:
    python exemple_pipeline.py
    
    ou avec paramètres personnalisés :
    
    python exemple_pipeline.py --query "machine learning" --days 14 --max-results 20
"""

import subprocess
import sys
import os
from datetime import datetime, timedelta
import argparse


def run_command(command, description):
    """
    Exécute une commande système avec gestion d'erreurs.
    
    Args:
        command (list): Commande à exécuter (format subprocess)
        description (str): Description de l'étape pour l'utilisateur
    
    Returns:
        bool: True si succès, False sinon
    """
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Commande: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} terminée avec succès")
        if result.stdout:
            print("Sortie:", result.stdout[-500:])  # Dernières 500 caractères
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}")
        print(f"Code d'erreur: {e.returncode}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Fichier Python non trouvé pour {description}")
        print("Vérifiez que vous êtes dans le bon répertoire")
        return False


def check_prerequisites():
    """
    Vérifie les prérequis avant l'exécution du pipeline.
    
    Returns:
        bool: True si tous les prérequis sont satisfaits
    """
    print("🔍 Vérification des prérequis...")
    
    # Vérification des fichiers Python
    required_files = [
        "1_search_tools.py",
        "2_analyse_sentiments.py", 
        "3_traduction.py",
        "4_analyse_fichier.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Fichier manquant: {file}")
            return False
    
    # Vérification de la clé API
    if not os.path.exists(".env"):
        print("❌ Fichier .env manquant")
        print("💡 Copiez .env.example vers .env et ajoutez votre clé NewsAPI")
        return False
    
    # Vérification des dépendances Python (basique)
    try:
        import requests
        import transformers
        import torch
        import tqdm
    except ImportError as e:
        print(f"❌ Dépendance Python manquante: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False
    
    print("✅ Tous les prérequis sont satisfaits")
    return True


def main():
    """
    Fonction principale qui orchestre l'exécution du pipeline complet.
    """
    parser = argparse.ArgumentParser(
        description="Exemple d'exécution complète du pipeline d'analyse de sentiment"
    )
    parser.add_argument(
        "--query", 
        default="intelligence artificielle",
        help="Terme de recherche pour les actualités (défaut: 'intelligence artificielle')"
    )
    parser.add_argument(
        "--days", 
        type=int, 
        default=7,
        help="Nombre de jours depuis aujourd'hui pour la recherche (défaut: 7)"
    )
    parser.add_argument(
        "--max-results", 
        type=int, 
        default=10,
        help="Nombre maximum d'articles à récupérer (défaut: 10)"
    )
    parser.add_argument(
        "--skip-collection",
        action="store_true",
        help="Ignorer la collecte d'actualités (utiliser les fichiers existants)"
    )
    
    args = parser.parse_args()
    
    print("🚀 PIPELINE D'ANALYSE DE SENTIMENT D'ACTUALITÉS")
    print("=" * 60)
    print(f"Requête: {args.query}")
    print(f"Période: {args.days} derniers jours")
    print(f"Max articles: {args.max_results}")
    
    # Vérification des prérequis
    if not check_prerequisites():
        print("\n❌ Impossible de continuer. Résolvez les problèmes ci-dessus.")
        sys.exit(1)
    
    # Calcul de la date de début
    from_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    
    success = True
    
    # Étape 1: Collecte d'actualités
    if not args.skip_collection:
        command = [
            sys.executable, "1_search_tools.py",
            args.query,
            "--from-date", from_date,
            "--max-results", str(args.max_results)
        ]
        success &= run_command(command, "Étape 1: Collecte d'actualités via NewsAPI")
    else:
        print("\n⏭️  Étape 1 ignorée: Collecte d'actualités")
    
    if not success:
        print("\n❌ Arrêt du pipeline à l'étape 1")
        sys.exit(1)
    
    # Étape 2: Analyse de sentiment
    command = [sys.executable, "2_analyse_sentiments.py"]
    success &= run_command(command, "Étape 2: Analyse de sentiment multilingue")
    
    if not success:
        print("\n❌ Arrêt du pipeline à l'étape 2")
        sys.exit(1)
    
    # Étape 3: Traduction automatique
    command = [sys.executable, "3_traduction.py"]
    success &= run_command(command, "Étape 3: Traduction automatique vers le français")
    
    if not success:
        print("\n❌ Arrêt du pipeline à l'étape 3")
        sys.exit(1)
    
    # Étape 4: Génération de rapport
    command = [sys.executable, "4_analyse_fichier.py", "resultats_sentiments_corpus_traduit.json"]
    success &= run_command(command, "Étape 4: Génération du rapport d'analyse")
    
    if success:
        print(f"\n{'='*60}")
        print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS!")
        print(f"{'='*60}")
        print("\n📁 Fichiers générés:")
        print("  • resultats_news.txt - Articles collectés")
        print("  • corpus_concatene.txt - Tous les titres extraits")
        print("  • resultats_sentiments_corpus.json - Analyse de sentiment")
        print("  • resultats_sentiments_corpus_traduit.json - Avec traductions")
        print("\n💡 Conseils pour la suite:")
        print("  • Examinez le rapport d'analyse affiché ci-dessus")
        print("  • Vérifiez manuellement quelques classifications")
        print("  • Comparez avec d'autres périodes ou requêtes")
        print("  • Utilisez les données JSON pour des analyses personnalisées")
    else:
        print(f"\n{'='*60}")
        print("❌ PIPELINE INTERROMPU")
        print(f"{'='*60}")
        print("Des erreurs sont survenues. Vérifiez les messages ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()

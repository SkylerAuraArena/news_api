"""
Module de recherche d'actualités via l'API NewsAPI.

Ce module permet de rechercher et récupérer des articles d'actualité 
en utilisant l'API NewsAPI. Il effectue des requêtes HTTP pour obtenir
des articles selon des critères spécifiques (mots-clés, date, tri, langue).

Dépendances:
- requests: pour les requêtes HTTP vers l'API NewsAPI
- python-dotenv: pour charger les variables d'environnement
- argparse: pour l'interface en ligne de commande

Variables d'environnement requises:
- NEWSAPI_KEY: clé d'API pour accéder à NewsAPI.org
"""

import os
from dotenv import load_dotenv
import requests

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération de la clé API NewsAPI depuis les variables d'environnement
API_KEY = os.getenv("NEWSAPI_KEY")
if not API_KEY:
    raise ValueError("NEWSAPI_KEY manquante. Veuillez définir cette variable dans votre fichier .env")

def format_news_context(query="Generative AI", from_date="2025-07-10", sort="relevancy", max_results=5):
    """
    Recherche et formate des articles d'actualité via l'API NewsAPI.
    
    Cette fonction effectue une requête vers l'API NewsAPI pour récupérer
    des articles selon les critères spécifiés, puis formate les résultats
    en une chaîne de caractères lisible.
    
    Args:
        query (str): Terme de recherche pour les articles (défaut: "Generative AI")
        from_date (str): Date de début au format YYYY-MM-DD (défaut: "2025-07-10")
        sort (str): Critère de tri ("relevancy", "popularity", "publishedAt")
        max_results (int): Nombre maximum d'articles à récupérer (défaut: 5)
    
    Returns:
        str: Articles formatés ou chaîne vide si aucun résultat/erreur
        
    Note:
        - La langue est fixée à 'zh' (chinois) dans cette version
        - Chaque article inclut: titre, source, date, description et URL
    """
    # Construction de l'URL de requête avec les paramètres
    url = (f'https://newsapi.org/v2/everything?'
           f'q={query}&'
           f'from={from_date}&'
           f'sortBy={sort}&'
           f'pageSize={max_results}&'
           f'language=zh&'  # Langue fixée en chinois
           f'apiKey={API_KEY}')
    
    # Exécution de la requête HTTP
    resp = requests.get(url)
    data = resp.json()
    
    # Vérification de la validité de la réponse
    if data.get("status") != "ok" or "articles" not in data:
        return ""
    
    # Formatage des articles en texte lisible
    # Structure: - Titre (Source, Date) — Description\n  URL
    return "\n".join(
        f"- {art['title']} ({art.get('source', {}).get('name','')}, {art['publishedAt'][:10]}) — {art.get('description','')}\n  {art['url']}"
        for art in data["articles"][:max_results]
    )

if __name__ == "__main__":
    """
    Interface en ligne de commande pour la recherche d'actualités.
    
    Permet d'utiliser le script directement depuis le terminal avec
    des arguments personnalisables pour la recherche.
    
    Exemple d'utilisation:
        python 1_search_tools.py "intelligence artificielle" --from-date 2025-07-01 --max-results 10
    """
    import argparse
    from datetime import datetime, timedelta

    # Configuration du parser d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Recherche d'actualités via NewsAPI")
    parser.add_argument("query", nargs="+", help="Texte à chercher (ex: 'générative AI')")
    parser.add_argument("--from-date", default=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                        help="Date de début (YYYY-MM-DD, défaut = il y a 7 jours)")
    parser.add_argument("--sort", default="relevancy", choices=["relevancy", "popularity", "publishedAt"],
                        help="Mode de tri (défaut: relevancy)")
    parser.add_argument("--max-results", type=int, default=5, help="Nombre d'articles (défaut: 5)")

    args = parser.parse_args()
    query_str = " ".join(args.query)  # Reconstitution de la requête depuis les arguments

    # Exécution de la recherche avec les paramètres fournis
    print(f"Recherche actualités pour : {query_str}\n")
    context = format_news_context(
        query=query_str,
        from_date=args.from_date,
        sort=args.sort,
        max_results=args.max_results
    )

    # Affichage des résultats
    if context:
        print(context)
    else:
        print("[Aucun résultat trouvé]")

    # Sauvegarde des résultats dans un fichier texte
    filename = "resultats_news.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(context)

    print(f"Les résultats ont été sauvegardés dans {filename}")
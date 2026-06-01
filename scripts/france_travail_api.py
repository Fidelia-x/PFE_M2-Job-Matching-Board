# identifiant client: PAR_jobmatching_0079a623d606e91e9dd17dd8c6ebdc3a3cf6ba0a4dd308c99a920b872339732e
# cle secrete: c7b10462ffffb3ba58d73cc7386716988370e7c6652b6c307ccce76ab85eb89d
import requests
import os

# Dans un projet réel, utilisez des variables d'environnement (.env)
CLIENT_ID = "PAR_jobmatching_0079a623d606e91e9dd17dd8c6ebdc3a3cf6ba0a4dd308c99a920b872339732e"
CLIENT_SECRET = "c7b10462ffffb3ba58d73cc7386716988370e7c6652b6c307ccce76ab85eb89d"

def get_access_token():
    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dOffre"
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

def fetch_jobs():
    token = get_access_token()
    if not token:
        return "Erreur d'authentification"
    
    headers = {"Authorization": f"Bearer {token}"}
    # Exemple de recherche pour des offres 'Développeur'
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?motsCles=developpeur"
    
    response = requests.get(url, headers=headers)
    return response.json()

# Test de récupération
jobs = fetch_jobs()
print(f"Nombre d'offres trouvées : {len(jobs.get('resultats', []))}")
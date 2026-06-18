from matching_cv import find_best_matches
from sentence_transformers import SentenceTransformer

def test_local():
    print("--- Test du moteur de matching ---")
    # Texte de test (simulant un CV)
    cv_text = "Je suis un développeur Python expert en Airflow et SQL, cherchant un poste de Data Engineer."
    
    try:
        matches = find_best_matches(cv_text, top_n=5)
        print(f"CV analysé : {cv_text}\n")
        
        if not matches:
            print("Aucun match trouvé. Vérifie si ta table 'offres_emploi' contient des données et des embeddings.")
        else:
            for m in matches:
                print(f"Offre trouvée : {m['titre']}")
                print(f"Entreprise : {m['company']}")
                print(f"Score de similarité : {m['score']}")
                print(f"Score de pertinence : {m['score'] * 100:.1f}%")
                print("-" * 30)
                
    except Exception as e:
        print(f"Erreur lors du test : {e}")

if __name__ == "__main__":
    test_local()
import json
import os

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            return None
        _client = Mistral(api_key=api_key)
    return _client


def get_skill_advice(missing_skills):
    """Pour une liste de compétences manquantes (labels, jamais le texte brut
    du CV — on n'envoie à Mistral que ce qui est nécessaire), génère un
    conseil court et une idée de projet par compétence.

    Contenu volontairement génératif (pas de nom de formation ni d'organisme
    réel demandé ici, voir scripts.training_catalog pour ça) : un LLM peut
    halluciner un cours qui n'existe pas, mais suggérer une idée de projet
    n'a pas de "bonne réponse" factuelle à inventer.

    Retourne {skill: {"conseil": str, "projet_suggere": str}}, ou {} si
    l'API n'est pas joignable (pas de clé, quota dépassé, erreur réseau) —
    l'appelant doit pouvoir afficher les recommandations sans cette partie.
    """
    if not missing_skills:
        return {}

    client = _get_client()
    if client is None:
        return {}

    prompt = f"""Pour chacune de ces compétences qu'un candidat data doit encore acquérir : {", ".join(missing_skills)}.

Propose en français, pour chaque compétence, un conseil court (une phrase) et une idée de projet concret et réalisable pour la pratiquer (une phrase).

Réponds uniquement avec un JSON strict de cette forme, sans texte autour :
{{"NomCompetence": {{"conseil": "...", "projet_suggere": "..."}}}}"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {}

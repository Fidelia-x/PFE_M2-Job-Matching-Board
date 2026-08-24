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
    conseil court et un projet détaillé (titre, étapes, livrable) par
    compétence.

    Contenu volontairement génératif (pas de nom de formation ni d'organisme
    réel demandé ici, voir scripts.training_catalog pour ça) : un LLM peut
    halluciner un cours qui n'existe pas, mais suggérer un projet n'a pas de
    "bonne réponse" factuelle à inventer — sauf pour les détails vérifiables
    (nom de jeu de données précis, URL, version d'outil) qu'on demande donc
    explicitement d'éviter dans le prompt.

    Retourne {skill: {"conseil": str, "projet": {"titre": str, "etapes":
    [str, ...], "livrable": str}}}, ou {} si l'API n'est pas joignable (pas
    de clé, quota dépassé, erreur réseau) — l'appelant doit pouvoir afficher
    les recommandations sans cette partie.
    """
    if not missing_skills:
        return {}

    client = _get_client()
    if client is None:
        return {}

    prompt = f"""Pour chacune de ces compétences qu'un candidat data doit encore acquérir : {", ".join(missing_skills)}.

Pour chaque compétence, propose en français :
- un conseil court (une phrase)
- un projet pour la pratiquer : un titre, 2 à 3 étapes concrètes et actionnables, et le livrable final attendu

Reste général et réalisable sans matériel spécifique : ne mentionne aucun nom précis de jeu de données, URL ou version d'outil que tu ne peux pas garantir exacte — décris plutôt le type de données ou d'outil à utiliser.

Réponds uniquement avec un JSON strict de cette forme, sans texte autour :
{{"NomCompetence": {{"conseil": "...", "projet": {{"titre": "...", "etapes": ["...", "...", "..."], "livrable": "..."}}}}}}"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        raw = json.loads(response.choices[0].message.content)
    except Exception:
        return {}

    # Mistral ne réécrit pas toujours la compétence avec exactement la même
    # casse qu'en entrée (ex. "Sql" envoyé, "SQL" reçu) — on retrouve la
    # correspondance insensible à la casse et on reclé sur le label exact
    # attendu par l'appelant, sinon .get(skill) raterait silencieusement.
    lookup = {key.lower(): value for key, value in raw.items()}
    return {skill: lookup[skill.lower()] for skill in missing_skills if skill.lower() in lookup}

from back_service.mistral_client import get_client

SYSTEM_PROMPT = """Tu es l'assistant IA de SkillGap, une plateforme d'aide à la recherche d'emploi dans la data (matching CV, offres, tendances du marché, recommandations de formations).

Ton rôle principal : aider l'utilisateur sur les sujets carrière, compétences et marché de l'emploi — expliquer ses résultats de matching, conseiller sur les compétences à développer, discuter du marché du travail. Tu peux aussi répondre à des questions plus générales si on te les pose, sans les refuser ni rediriger systématiquement vers le sujet emploi.

Réponds en français, de façon concise et chaleureuse."""


def _build_context_block(profile_context):
    if not profile_context:
        return ""
    lines = ["Contexte du candidat connecté à utiliser seulement si pertinent pour répondre (ne le mentionne pas si la question n'a aucun rapport) :"]
    if profile_context.get("score") is not None:
        lines.append(f"- Meilleur score de correspondance avec une offre du marché : {profile_context['score']}%")
    if profile_context.get("compatible_count") is not None:
        lines.append(f"- Nombre d'offres compatibles (score >= 70%) : {profile_context['compatible_count']}")
    if profile_context.get("missing_skills"):
        lines.append(f"- Compétences manquantes les plus fréquentes dans les offres du candidat : {', '.join(profile_context['missing_skills'])}")
    return "\n".join(lines)


def stream_chat_reply(messages, profile_context=None):
    """messages : historique de la conversation (liste de {"role": "user"|"assistant", "content": str}),
    sans le system prompt — ajouté ici à chaque appel.

    profile_context : dict optionnel avec les résultats de matching du candidat
    (score, compatible_count, missing_skills — jamais le texte du CV), injecté
    dans le system prompt pour ancrer les réponses sur son profil réel.

    Retourne un générateur de morceaux de texte à streamer, ou None si
    Mistral n'est pas joignable (pas de clé, quota dépassé, erreur réseau) —
    l'appelant doit pouvoir dégrader proprement plutôt que planter."""
    client = get_client()
    if client is None:
        return None

    system_content = SYSTEM_PROMPT
    context_block = _build_context_block(profile_context)
    if context_block:
        system_content += "\n\n" + context_block

    full_messages = [{"role": "system", "content": system_content}] + messages

    try:
        stream = client.chat.stream(model="mistral-small-latest", messages=full_messages)
    except Exception:
        return None

    def _generate():
        try:
            for event in stream:
                delta = event.data.choices[0].delta.content
                if delta:
                    yield delta
        except Exception:
            yield "\n\n*(La réponse a été interrompue — problème de connexion à l'assistant.)*"

    return _generate()

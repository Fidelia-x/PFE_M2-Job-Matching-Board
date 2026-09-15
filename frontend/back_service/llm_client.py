import os

from dotenv import load_dotenv
from groq import Groq
# from mistralai.client import Mistral

load_dotenv()

_client = None


def get_client():
    """Client Groq partagé (singleton paresseux), réutilisé par tous les
    back_services qui appellent le LLM. Retourne None si GROQ_API_KEY n'est
    pas configurée — aux appelants de dégrader proprement plutôt que planter."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        _client = Groq(api_key=api_key)
        # api_key = os.getenv("MISTRAL_API_KEY")
        # if not api_key:
        #     return None
        # _client = Mistral(api_key=api_key)
    return _client

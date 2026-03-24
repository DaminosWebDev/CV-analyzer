# backend/app/services/llm_service.py
# Rôle       : Service d'appel au LLM via Groq API
# Dépendances: groq, app.config

from groq import Groq, AsyncGroq
from typing import AsyncGenerator
from app.config import get_settings

# Instance du client Groq — créée une seule fois au démarrage
settings = get_settings()

# Client synchrone — pour les appels normaux
_groq_client = Groq(api_key=settings.groq_api_key)

# Client asynchrone — pour le streaming SSE
_groq_async_client = AsyncGroq(api_key=settings.groq_api_key)


def call_llm(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.3,
) -> str:
    """
    Appel synchrone au LLM — retourne la réponse complète.
    Utilisé pour les analyses JSON structurées.

    Args:
        system_prompt: instructions de comportement pour le LLM
        user_prompt: la requête de l'utilisateur
        max_tokens: limite de longueur de la réponse
        temperature: créativité (0 = déterministe, 1 = créatif)

    Returns:
        texte de la réponse du LLM

    Raises:
        RuntimeError: si l'appel API échoue
    """
    try:
        response = _groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Erreur appel LLM : {str(e)}")


async def stream_llm(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """
    Appel asynchrone au LLM avec streaming — retourne les tokens un par un.
    Utilisé pour l'endpoint SSE /analyze/stream.

    Args:
        system_prompt: instructions de comportement pour le LLM
        user_prompt: la requête de l'utilisateur
        max_tokens: limite de longueur de la réponse
        temperature: créativité

    Yields:
        chaque token de texte au fur et à mesure qu'il arrive
    """
    try:
        # stream=True active le mode streaming
        stream = await _groq_async_client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        # On itère sur les chunks reçus un par un
        async for chunk in stream:
            # Chaque chunk peut contenir un token ou être vide
            token = chunk.choices[0].delta.content
            if token is not None:
                yield token

    except Exception as e:
        # En cas d'erreur pendant le stream, on yield un message d'erreur
        yield f"\n[ERREUR STREAM : {str(e)}]"


def check_llm_connection() -> dict:
    """
    Vérifie que la connexion Groq fonctionne.
    Utilisé par l'endpoint /health.

    Returns:
        dict avec status et model
    """
    try:
        response = _groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": "Réponds uniquement : OK"}],
            max_tokens=5,
        )
        answer = response.choices[0].message.content.strip()
        return {
            "status": "connected",
            "model": settings.groq_model,
            "test_response": answer
        }
    except Exception as e:
        return {
            "status": "error",
            "model": settings.groq_model,
            "error": str(e)
        }
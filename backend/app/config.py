# backend/app/config.py
# Rôle       : Gestion centralisée de la configuration et variables d'environnement
# Dépendances: pydantic-settings, python-dotenv

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Classe de configuration — lit automatiquement le fichier .env
    Chaque attribut correspond à une variable d'environnement
    """

    # ── API Groq ──────────────────────────────────────────────────────────────
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # ── Application ───────────────────────────────────────────────────────────
    environment: str = "development"
    app_name: str = "CV-Analyzer-AI"
    app_version: str = "1.0.0"

    # ── CORS — origines autorisées à appeler l'API ────────────────────────────
    allowed_origins: list[str] = [
        "http://localhost:3000",   # Next.js en développement local
        "http://localhost:3001",
    ]

    class Config:
        # Indique où trouver le fichier .env
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Ignore les variables d'environnement inconnues (évite les erreurs)
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Retourne l'instance de configuration — mise en cache après le premier appel.
    Utiliser cette fonction plutôt que d'instancier Settings() directement.
    """
    return Settings()


# Instance globale — importable directement si besoin
settings = get_settings()
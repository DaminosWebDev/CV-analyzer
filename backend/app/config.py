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

    # ── URL frontend Vercel ───────────────────────────────────────────────────
    # Sera renseignée via variable d'environnement sur Render
    # Exemple : https://cv-analyzer-ai.vercel.app
    frontend_url: str = ""

    # ── CORS — origines autorisées à appeler l'API ────────────────────────────
    # Les origines fixes (toujours présentes)
    _base_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    @property
    def allowed_origins(self) -> list[str]:
        """
        Construit dynamiquement la liste des origines autorisées.
        Fusionne les origines fixes + l'URL Vercel si elle est définie.
        """
        origins = list(self._base_origins)

        # Ajoute l'URL Vercel si la variable d'environnement est renseignée
        if self.frontend_url:
            origins.append(self.frontend_url)

        return origins

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
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
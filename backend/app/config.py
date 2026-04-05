# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # ── API Groq ──────────────────────────────────────────────────────────────
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # ── Application ───────────────────────────────────────────────────────────
    environment: str = "development"
    app_name: str = "CV-Analyzer-AI"
    app_version: str = "1.0.0"

    # ── URL frontend Vercel ───────────────────────────────────────────────────
    frontend_url: str = ""

    # ── CORS ──────────────────────────────────────────────────────────────────
    # Champ Pydantic valide (sans underscore)
    base_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    @property
    def allowed_origins(self) -> list[str]:
        origins = list(self.base_origins)
        if self.frontend_url:
            origins.append(self.frontend_url.rstrip("/"))  # évite les slash finaux
        return origins

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
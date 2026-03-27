# backend/app/main.py
# Rôle       : Point d'entrée principal de l'application FastAPI
# Dépendances: fastapi, app.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze
from app.config import settings

# ── Création de l'application FastAPI ────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## CV-Analyzer-AI 🎯

API d'analyse de compatibilité entre un CV et une offre d'emploi via IA.

### Fonctionnalités
- 📄 **Upload CV** : PDF ou texte brut
- 🎯 **Score de match** : compatibilité 0-100%
- 🔑 **Mots-clés** : présents et manquants
- 💡 **Conseils** : amélioration concrète par section
- ⚡ **Streaming SSE** : réponse en temps réel

### Stack technique
- **LLM** : LLaMA 3.3 70b via Groq API
- **Backend** : FastAPI async
- **Parsing PDF** : PyMuPDF
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Configuration CORS ────────────────────────────────────────────────────────
# allowed_origins est maintenant une @property dans config.py
# Elle fusionne automatiquement localhost + l'URL Vercel (si définie)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Enregistrement des routers ────────────────────────────────────────────────
app.include_router(analyze.router)

# ── Routes de base ────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Point d'entrée — vérifie que l'API est en ligne"""
    return {
        "message": f"Bienvenue sur {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "status": "online"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de santé — utilisé par Render pour vérifier que l'app tourne"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "model": settings.groq_model,
    }
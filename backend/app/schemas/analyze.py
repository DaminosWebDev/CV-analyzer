# backend/app/schemas/analyze.py
# Rôle       : Modèles de données Pydantic pour l'analyse CV/offre
# Dépendances: pydantic

from pydantic import BaseModel, Field
from typing import Optional


# ═══════════════════════════════════════════════════════════
# SCHEMAS D'ENTRÉE — ce que l'utilisateur envoie
# ═══════════════════════════════════════════════════════════

class AnalyzeRequest(BaseModel):
    """
    Données envoyées par le frontend pour déclencher une analyse.
    Le CV peut être fourni en texte OU en PDF (upload séparé).
    """
    cv_text: str = Field(
        ...,                          # ... = champ obligatoire
        min_length=50,
        max_length=15000,
        description="Texte brut du CV (extrait du PDF ou saisi directement)"
    )
    job_offer: str = Field(
        ...,
        min_length=50,
        max_length=10000,
        description="Texte de l'offre d'emploi"
    )
    language: str = Field(
        default="fr",
        description="Langue de l'analyse : 'fr' ou 'en'"
    )

    class Config:
        # Exemple affiché dans la doc Swagger
        json_schema_extra = {
            "example": {
                "cv_text": "Jean Dupont - Développeur Python\n5 ans d'expérience FastAPI, React...",
                "job_offer": "Nous recherchons un développeur Full-Stack Python/React...",
                "language": "fr"
            }
        }


# ═══════════════════════════════════════════════════════════
# SCHEMAS DE SORTIE — ce que l'API retourne
# ═══════════════════════════════════════════════════════════

class KeywordsResult(BaseModel):
    """Mots-clés extraits du CV et de l'offre"""
    present: list[str] = Field(
        default=[],
        description="Compétences du CV qui matchent l'offre"
    )
    missing: list[str] = Field(
        default=[],
        description="Compétences requises par l'offre absentes du CV"
    )
    bonus: list[str] = Field(
        default=[],
        description="Compétences du CV non demandées mais valorisantes"
    )


class SectionAnalysis(BaseModel):
    """Analyse détaillée d'une section du CV"""
    score: int = Field(
        ...,
        ge=0,    # greater or equal — minimum 0
        le=100,  # less or equal — maximum 100
        description="Score de cette section (0-100)"
    )
    strengths: list[str] = Field(
        default=[],
        description="Points forts de cette section"
    )
    improvements: list[str] = Field(
        default=[],
        description="Axes d'amélioration pour cette section"
    )


class AnalyzeResult(BaseModel):
    """
    Résultat complet de l'analyse CV/offre.
    C'est ce que l'endpoint /analyze retourne.
    """
    # Score global
    match_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Score global de compatibilité (0-100)"
    )
    match_level: str = Field(
        ...,
        description="Niveau textuel : 'Excellent' | 'Bon' | 'Moyen' | 'Faible'"
    )

    # Mots-clés
    keywords: KeywordsResult

    # Analyse par section
    sections: dict[str, SectionAnalysis] = Field(
        default={},
        description="Analyse par section : experience, education, skills, summary"
    )

    # Conseils
    top_recommendations: list[str] = Field(
        default=[],
        description="Top 3-5 conseils prioritaires"
    )
    detailed_advice: str = Field(
        default="",
        description="Conseils détaillés (peut être streamé)"
    )

    # Métadonnées
    language: str = "fr"
    model_used: str = ""


class AnalyzeResponse(BaseModel):
    """Enveloppe standard pour toutes les réponses de l'API"""
    success: bool = True
    data: Optional[AnalyzeResult] = None
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════
# SCHEMA POUR L'UPLOAD PDF
# ═══════════════════════════════════════════════════════════

class PDFExtractResponse(BaseModel):
    """Réponse après extraction du texte d'un PDF"""
    success: bool
    text: Optional[str] = None
    char_count: int = 0
    page_count: int = 0
    error: Optional[str] = None
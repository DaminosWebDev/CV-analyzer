# backend/app/schemas/analyze.py
# Rôle : définit la structure des données échangées via l'API
# Dépendances : pydantic

from pydantic import BaseModel, Field
from typing import List, Optional


class PDFExtractResponse(BaseModel):
    """Réponse de l'endpoint POST /upload-cv"""
    success: bool = True
    text: str = Field(default="", description="Texte extrait du PDF")
    char_count: int = Field(default=0, description="Nombre de caractères extraits")
    page_count: int = Field(default=0, description="Nombre de pages du PDF")
    error: Optional[str] = Field(default=None, description="Message d'erreur si échec")


class AnalyzeRequest(BaseModel):
    """Ce que l'utilisateur envoie à l'API."""
    cv_text: str = Field(..., description="Texte brut du CV")
    job_offer: str = Field(..., description="Texte brut de l'offre d'emploi")

class StreamRequest(BaseModel):
    """
    Ce que le frontend envoie à POST /analyze/stream.
    Contient le CV + l'offre + les résultats déjà calculés par /analyze.

    Pourquoi passer score et points_faibles ?
    Le frontend appelle d'abord /analyze (JSON complet),
    puis /analyze/stream (conseils streaming).
    On réutilise les résultats du premier appel pour le second
    plutôt que de tout recalculer — plus rapide et cohérent.
    """
    cv_text: str = Field(..., description="Texte brut du CV")
    job_offer: str = Field(..., description="Texte brut de l'offre d'emploi")
    score: int = Field(default=0, description="Score calculé par /analyze")
    points_faibles: List[str] = Field(default=[], description="Points faibles calculés par /analyze")


# NOUVEAU : structure imbriquée pour les compétences
class CompetencesDetail(BaseModel):
    """Compétences présentes et manquantes pour une catégorie."""
    presentes: List[str] = Field(default=[], description="Présentes dans le CV et demandées")
    manquantes: List[str] = Field(default=[], description="Demandées mais absentes du CV")


class KeywordsResult(BaseModel):
    """Résultat de l'extraction des mots-clés."""
    techniques: CompetencesDetail = Field(default_factory=CompetencesDetail)
    soft_skills: CompetencesDetail = Field(default_factory=CompetencesDetail)


class AnalyzeResult(BaseModel):
    """Résultat complet de l'analyse."""

    # Bloc 1 : scoring
    score: int = Field(default=0, ge=0, le=100, description="Score de match de 0 à 100")
    niveau: str = Field(default="Non déterminé", description="Niveau de match en texte")
    points_forts: List[str] = Field(default=[], description="Points forts du CV")
    points_faibles: List[str] = Field(default=[], description="Points faibles / manques")
    justification: str = Field(default="", description="Explication du score en 2-3 phrases")

    # Bloc 2 : mots-clés avec structure détaillée
    keywords: KeywordsResult = Field(
        default_factory=KeywordsResult,
        description="Compétences techniques et soft skills extraites"
    )

    # Bloc 3 : conseils (vide pour l'instant)
    conseils: str = Field(default="", description="Conseils d'amélioration")


class AnalyzeResponse(BaseModel):
    """Enveloppe la réponse API avec métadonnées."""
    success: bool = True
    data: AnalyzeResult
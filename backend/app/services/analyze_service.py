# backend/app/services/analyze_service.py
# Rôle       : Orchestration de l'analyse CV/offre via LLM
# Dépendances: app.services.llm_service, app.schemas.analyze

import json
import re
from typing import AsyncGenerator

from app.services.llm_service import call_llm, stream_llm
from app.schemas.analyze import (
    AnalyzeResult,
    KeywordsResult,
    SectionAnalysis,
)


# ═══════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT_ANALYSIS = """Tu es un expert RH et recruteur senior avec 15 ans d'expérience.
Tu analyses la compatibilité entre un CV et une offre d'emploi.
Tu réponds TOUJOURS en JSON valide, sans texte avant ou après le JSON.
Sois précis, objectif et actionnable dans tes analyses."""

SYSTEM_PROMPT_ADVICE = """Tu es un coach carrière expert, bienveillant et direct.
Tu donnes des conseils concrets et actionnables pour améliorer un CV.
Tu écris en français, avec un ton professionnel mais accessible.
Tu structures tes conseils par priorité d'impact."""


def build_analysis_prompt(cv_text: str, job_offer: str) -> str:
    """
    Construit le prompt principal pour l'analyse CV/offre.
    Demande une réponse JSON structurée.
    """
    return f"""Analyse la compatibilité entre ce CV et cette offre d'emploi.

=== CV ===
{cv_text}

=== OFFRE D'EMPLOI ===
{job_offer}

Réponds UNIQUEMENT avec ce JSON (sans markdown, sans texte avant/après) :
{{
    "match_score": <entier 0-100>,
    "match_level": "<Excellent|Bon|Moyen|Faible>",
    "keywords": {{
        "present": ["compétence1", "compétence2"],
        "missing": ["compétence1", "compétence2"],
        "bonus": ["compétence1", "compétence2"]
    }},
    "sections": {{
        "experience": {{
            "score": <0-100>,
            "strengths": ["point fort 1"],
            "improvements": ["amélioration 1"]
        }},
        "education": {{
            "score": <0-100>,
            "strengths": ["point fort 1"],
            "improvements": ["amélioration 1"]
        }},
        "skills": {{
            "score": <0-100>,
            "strengths": ["point fort 1"],
            "improvements": ["amélioration 1"]
        }},
        "summary": {{
            "score": <0-100>,
            "strengths": ["point fort 1"],
            "improvements": ["amélioration 1"]
        }}
    }},
    "top_recommendations": [
        "Conseil prioritaire 1",
        "Conseil prioritaire 2",
        "Conseil prioritaire 3"
    ]
}}"""


def build_advice_prompt(cv_text: str, job_offer: str, match_score: int) -> str:
    """
    Construit le prompt pour les conseils détaillés streamés.
    Ce prompt génère du texte narratif (pas du JSON).
    """
    return f"""Un candidat a soumis son CV pour une offre d'emploi.
Score de compatibilité calculé : {match_score}/100.

=== CV ===
{cv_text[:3000]}

=== OFFRE D'EMPLOI ===
{job_offer[:2000]}

Rédige des conseils détaillés et actionnables pour améliorer ce CV.
Structure ta réponse ainsi :

## 🎯 Analyse globale
[2-3 phrases sur le niveau de compatibilité]

## ✅ Points forts à valoriser
[Liste des atouts du candidat par rapport à l'offre]

## 🔧 Améliorations prioritaires
[Conseils concrets section par section]

## 💡 Formulations suggérées
[Exemples de phrases à ajouter/modifier dans le CV]

## 🚀 Plan d'action
[3 actions concrètes à faire cette semaine]"""


# ═══════════════════════════════════════════════════════════
# PARSING DE LA RÉPONSE JSON
# ═══════════════════════════════════════════════════════════

def parse_llm_json(raw_response: str) -> dict:
    """
    Parse la réponse JSON du LLM de façon robuste.
    Gère les cas où le LLM ajoute du texte avant/après le JSON.

    Args:
        raw_response: texte brut retourné par le LLM

    Returns:
        dict Python parsé depuis le JSON

    Raises:
        ValueError: si aucun JSON valide n'est trouvable
    """
    # Tentative 1 : parse direct
    try:
        return json.loads(raw_response.strip())
    except json.JSONDecodeError:
        pass

    # Tentative 2 : extraction entre ```json ... ```
    json_match = re.search(r"```json\s*(.*?)\s*```", raw_response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Tentative 3 : extraction entre { et } (premier bloc JSON)
    json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Impossible de parser la réponse du LLM en JSON. "
        f"Réponse reçue : {raw_response[:200]}..."
    )


def build_analyze_result(data: dict) -> AnalyzeResult:
    """
    Convertit le dict JSON du LLM en objet AnalyzeResult Pydantic.
    Gère les valeurs manquantes avec des valeurs par défaut.

    Args:
        data: dict parsé depuis la réponse JSON du LLM

    Returns:
        AnalyzeResult validé par Pydantic
    """
    # Construction des mots-clés
    keywords_data = data.get("keywords", {})
    keywords = KeywordsResult(
        present=keywords_data.get("present", []),
        missing=keywords_data.get("missing", []),
        bonus=keywords_data.get("bonus", []),
    )

    # Construction des sections
    sections = {}
    sections_data = data.get("sections", {})
    for section_name, section_data in sections_data.items():
        sections[section_name] = SectionAnalysis(
            score=section_data.get("score", 50),
            strengths=section_data.get("strengths", []),
            improvements=section_data.get("improvements", []),
        )

    # Détermination du niveau textuel
    score = data.get("match_score", 0)
    if "match_level" in data:
        match_level = data["match_level"]
    else:
        # Calcul automatique si absent
        if score >= 80:
            match_level = "Excellent"
        elif score >= 60:
            match_level = "Bon"
        elif score >= 40:
            match_level = "Moyen"
        else:
            match_level = "Faible"

    return AnalyzeResult(
        match_score=max(0, min(100, score)),  # clamp entre 0 et 100
        match_level=match_level,
        keywords=keywords,
        sections=sections,
        top_recommendations=data.get("top_recommendations", []),
        language="fr",
    )


# ═══════════════════════════════════════════════════════════
# FONCTIONS PRINCIPALES
# ═══════════════════════════════════════════════════════════

def analyze_cv(cv_text: str, job_offer: str) -> AnalyzeResult:
    """
    Analyse complète CV/offre — retourne le résultat JSON complet.
    Appel synchrone — attend la réponse complète du LLM.

    Args:
        cv_text: texte brut du CV
        job_offer: texte de l'offre d'emploi

    Returns:
        AnalyzeResult complet

    Raises:
        RuntimeError: si l'analyse échoue
    """
    try:
        # Étape 1 : appel LLM pour l'analyse structurée
        prompt = build_analysis_prompt(cv_text, job_offer)
        raw_response = call_llm(
            system_prompt=SYSTEM_PROMPT_ANALYSIS,
            user_prompt=prompt,
            max_tokens=2000,
            temperature=0.2,  # très déterministe pour le JSON
        )

        # Étape 2 : parse du JSON
        data = parse_llm_json(raw_response)

        # Étape 3 : construction de l'objet Pydantic
        result = build_analyze_result(data)

        return result

    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'analyse CV : {str(e)}")


async def stream_advice(
    cv_text: str,
    job_offer: str,
    match_score: int,
) -> AsyncGenerator[str, None]:
    """
    Génère les conseils détaillés en streaming SSE.
    Appel asynchrone — retourne les tokens un par un.

    Args:
        cv_text: texte brut du CV
        job_offer: texte de l'offre d'emploi
        match_score: score calculé lors de l'analyse

    Yields:
        tokens de texte au fur et à mesure
    """
    prompt = build_advice_prompt(cv_text, job_offer, match_score)

    async for token in stream_llm(
        system_prompt=SYSTEM_PROMPT_ADVICE,
        user_prompt=prompt,
        max_tokens=2000,
        temperature=0.7,
    ):
        yield token
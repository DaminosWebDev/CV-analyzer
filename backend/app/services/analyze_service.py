# backend/app/services/analyze_service.py
# Rôle : orchestrateur principal — appelle les prompts et assemble le résultat
# Dépendances : llm_service, prompts/scoring_prompt, prompts/keywords_prompt, prompts/advice_prompt

from app.services.llm_service import call_llm_json, call_llm_stream
from app.prompts.scoring_prompt import build_scoring_prompt
from app.prompts.keywords_prompt import build_keywords_prompt
from app.prompts.advice_prompt import build_advice_prompt
from app.schemas.analyze import AnalyzeResult, KeywordsResult, CompetencesDetail


async def analyze_cv(cv_text: str, job_offer: str) -> AnalyzeResult:
    """
    Analyse complète — scoring + keywords.
    Retourne un AnalyzeResult JSON complet.
    """

    # --- APPEL 1 : Scoring ---
    scoring_prompt = build_scoring_prompt(cv_text, job_offer)
    scoring_result = await call_llm_json(scoring_prompt)

    # --- APPEL 2 : Extraction mots-clés ---
    keywords_prompt = build_keywords_prompt(cv_text, job_offer)
    keywords_raw = await call_llm_json(keywords_prompt)

    techniques_data = keywords_raw.get("techniques", {})
    soft_skills_data = keywords_raw.get("soft_skills", {})

    keywords = KeywordsResult(
        techniques=CompetencesDetail(
            presentes=techniques_data.get("presentes", []),
            manquantes=techniques_data.get("manquantes", []),
        ),
        soft_skills=CompetencesDetail(
            presentes=soft_skills_data.get("presentes", []),
            manquantes=soft_skills_data.get("manquantes", []),
        ),
    )

    return AnalyzeResult(
        score=scoring_result.get("score", 0),
        niveau=scoring_result.get("niveau", "Non déterminé"),
        points_forts=scoring_result.get("points_forts", []),
        points_faibles=scoring_result.get("points_faibles", []),
        justification=scoring_result.get("justification", ""),
        keywords=keywords,
        conseils=""
    )


async def stream_advice(cv_text: str, job_offer: str, score: int, points_faibles: list):
    """
    Génère les conseils d'amélioration en streaming token par token.

    Cette fonction est un générateur async — elle yield les tokens
    au fur et à mesure qu'ils arrivent de Groq.

    Appelée par l'endpoint POST /analyze/stream du router.

    Args:
        cv_text       : texte brut du CV
        job_offer     : texte brut de l'offre d'emploi
        score         : score déjà calculé par analyze_cv()
        points_faibles: points faibles déjà calculés par analyze_cv()

    Yields:
        str : chaque token de texte des conseils
    """
    prompt = build_advice_prompt(
        cv_text=cv_text,
        job_offer=job_offer,
        score=score,
        points_faibles=points_faibles,
    )

    # On propage les tokens un par un depuis call_llm_stream
    # "async for" = itération sur un générateur async
    async for token in call_llm_stream(prompt):
        yield token
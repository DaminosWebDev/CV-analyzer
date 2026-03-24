# backend/app/routers/analyze.py
# Rôle       : Endpoints FastAPI pour l'analyse CV/offre
# Dépendances: fastapi, app.services, app.schemas

import json
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from app.schemas.analyze import (
    AnalyzeRequest,
    AnalyzeResponse,
    PDFExtractResponse,
)
from app.services.analyze_service import analyze_cv, stream_advice
from app.services.pdf_service import extract_text_from_pdf

# ── Création du router ────────────────────────────────────────────────────────
# Un router est un "mini-app" FastAPI qu'on branche sur l'app principale
router = APIRouter(
    prefix="/api/v1",        # toutes les routes commencent par /api/v1
    tags=["Analysis"],       # groupe dans la doc Swagger
)


# ═══════════════════════════════════════════════════════════
# ENDPOINT 1 : Upload PDF
# ═══════════════════════════════════════════════════════════

@router.post("/upload-cv", response_model=PDFExtractResponse)
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload un fichier PDF et extrait son texte.
    Retourne le texte brut pour l'afficher dans le frontend.
    """
    # Vérification du type de fichier
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers PDF sont acceptés"
        )

    # Lecture du fichier en mémoire
    file_bytes = await file.read()

    # Extraction du texte
    try:
        text, page_count = extract_text_from_pdf(file_bytes)
        return PDFExtractResponse(
            success=True,
            text=text,
            char_count=len(text),
            page_count=page_count,
        )
    except ValueError as e:
        return PDFExtractResponse(
            success=False,
            error=str(e),
        )


# ═══════════════════════════════════════════════════════════
# ENDPOINT 2 : Analyse complète (JSON)
# ═══════════════════════════════════════════════════════════

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyse la compatibilité entre un CV et une offre d'emploi.
    Retourne le résultat complet en JSON (score, mots-clés, conseils).
    """
    try:
        result = analyze_cv(
            cv_text=request.cv_text,
            job_offer=request.job_offer,
        )
        return AnalyzeResponse(
            success=True,
            data=result,
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ═══════════════════════════════════════════════════════════
# ENDPOINT 3 : Streaming SSE
# ═══════════════════════════════════════════════════════════

@router.post("/analyze/stream")
async def analyze_stream(request: AnalyzeRequest):
    """
    Génère les conseils détaillés en streaming SSE.
    Les tokens arrivent en temps réel dans le frontend.

    Format SSE : chaque message est préfixé par 'data: '
    """

    async def event_generator():
        """Générateur SSE — formate chaque token en message SSE"""
        try:
            async for token in stream_advice(
                cv_text=request.cv_text,
                job_offer=request.job_offer,
                match_score=75,  # valeur par défaut — idéalement passée par le frontend
            ):
                # Format SSE standard : "data: <contenu>\n\n"
                yield f"data: {json.dumps({'token': token})}\n\n"

            # Signal de fin de stream
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            # Désactive la mise en cache — le stream doit arriver en temps réel
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # important pour Nginx/Render
        }
    )
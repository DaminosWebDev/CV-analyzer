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
    StreamRequest,
)
from app.services.analyze_service import analyze_cv, stream_advice
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"],
)


# ═══════════════════════════════════════════════════════════
# ENDPOINT 1 : Upload PDF
# ═══════════════════════════════════════════════════════════

@router.post("/upload-cv", response_model=PDFExtractResponse)
async def upload_cv(file: UploadFile = File(...)):
    """Upload un fichier PDF et extrait son texte."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers PDF sont acceptés"
        )

    file_bytes = await file.read()

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
    """Analyse la compatibilité entre un CV et une offre d'emploi."""
    try:
        # ⚠️ CORRECTION : await obligatoire car analyze_cv est async
        result = await analyze_cv(
            cv_text=request.cv_text,
            job_offer=request.job_offer,
        )
        return AnalyzeResponse(
            success=True,
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════
# ENDPOINT 3 : Streaming SSE
# ═══════════════════════════════════════════════════════════

@router.post("/analyze/stream")
async def analyze_stream(request: StreamRequest):
    """
    Génère les conseils d'amélioration en streaming SSE token par token.
    Le frontend reçoit chaque mot dès qu'il est généré par le LLM.
    """

    async def event_generator():
        try:
            async for token in stream_advice(
                cv_text=request.cv_text,
                job_offer=request.job_offer,
                score=request.score,
                points_faibles=request.points_faibles,
            ):
                yield f"data: {json.dumps({'token': token})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
"""Standards recommendation API endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import RecommendRequest, RecommendResponse
from app.services.matcher import recommend_standards
from app.services.translator import detect_language, translate_to_english

router = APIRouter(prefix="/api/standards", tags=["standards"])


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    """Recommend applicable IS standards based on product description."""
    lang = req.language or detect_language(req.product_description)
    query_en = translate_to_english(req.product_description, lang) if lang != "en" else req.product_description

    recs = recommend_standards(query_en, top_k=5)
    return RecommendResponse(recommendations=recs, query=req.product_description)

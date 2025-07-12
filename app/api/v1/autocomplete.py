# app/api/v1/autocomplete.py
from fastapi import APIRouter, Query
from app.services.ticker_resolver import suggest

router = APIRouter(tags=["autocomplete"])


@router.get("/autocomplete", summary="@ticker suggestions")
async def autocomplete(q: str = Query(..., min_length=1), limit: int = 8):
    """
    GET /v1/autocomplete?q=appl
    """
    return await suggest(q, limit)

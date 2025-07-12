# app/api/v1/health.py
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core import db

router = APIRouter(tags=["health"])


@router.get("/health", summary="Liveness / readiness probe")
async def health():
    """
    • Always returns 200 OK so load-balancers don’t evict the pod for
      a transient DB hiccup.
    • The JSON payload includes a simple "supabase": true/false flag.
    """
    db_ok = True
    if settings.data_source == "supabase":
        try:
            async with db.pool.acquire() as conn:
                await conn.execute("SELECT 1")   # 0-cost ping
        except Exception:
            db_ok = False

    overall = "ok" if db_ok else "degraded"
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": overall, "supabase": db_ok},
    )

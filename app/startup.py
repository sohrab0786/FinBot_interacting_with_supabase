# app/startup.py
from fastapi import FastAPI
from app.core import db
from app.core.config import settings


def register_startup_shutdown(app: FastAPI) -> None:
    """Attach DB + Supabase pool lifecycle handlers to a FastAPI app."""
    @app.on_event("startup")
    async def _startup() -> None:
        if settings.data_source == "supabase":
            db.init_supabase()
            await db.init_pool()
        print("🚀 Startup complete — data_source:", settings.data_source)

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        if db.pool:
            await db.close_pool()
        print("🛑 Shutdown complete")

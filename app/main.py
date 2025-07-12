# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.startup import register_startup_shutdown
from app.api.v1 import router as api_v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Financial Chat Agent",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS (relax in dev, tighten in prod)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount v1 API
    app.include_router(api_v1_router, prefix="/v1")

    # DB/Pool lifecycle
    register_startup_shutdown(app)
    return app


app = create_app()   # ← Uvicorn imports this symbol

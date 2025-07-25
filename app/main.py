from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ✅ ADD THIS

from app.startup import register_startup_shutdown
from app.api.v1 import router as api_v1_router
from app.api.ui import router as ui_router
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="Financial Chat Agent",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount routers
    app.include_router(api_v1_router, prefix="/v1")
    app.include_router(ui_router)

    # ✅ MOUNT static responses folder for direct access (optional)
    app.mount("/responses", StaticFiles(directory="responses"), name="responses")

    # Lifecycle hooks
    register_startup_shutdown(app)
    return app

app = create_app()

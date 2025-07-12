# app/api/v1/__init__.py
from fastapi import APIRouter
from . import chat, health          # import every sub-router module here

router = APIRouter()
router.include_router(chat.router,   prefix="/chat")   # POST /v1/chat/…
router.include_router(health.router)

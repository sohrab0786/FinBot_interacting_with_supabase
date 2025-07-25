# app/api/v1/__init__.py
from fastapi import APIRouter
from . import chat, health, autocomplete

router = APIRouter()
router.include_router(chat.router)  # ✅ No prefix
router.include_router(health.router)
router.include_router(autocomplete.router)
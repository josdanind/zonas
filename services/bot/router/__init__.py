# FastAPI
from fastapi import APIRouter

# Bot Routes
from .webhook import router as webhook_router

router = APIRouter()

# Add routes to bot router
router.include_router(webhook_router)

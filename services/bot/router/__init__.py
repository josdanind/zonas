# FastAPI
from fastapi import APIRouter

# Bot Routes
from .webhook import router as webhook_router
from .bot_actions.router import router as bot_actions_router

router = APIRouter()

# Add routes to bot router
router.include_router(webhook_router)
router.include_router(bot_actions_router)

# FastAPI
from fastapi import APIRouter

# Routers
from .bots.router import router as bots_router

router = APIRouter()

# Addinf router
router.include_router(bots_router)

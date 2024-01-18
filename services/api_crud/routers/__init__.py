# FastAPI
from fastapi import APIRouter

# Routers
from .bots.router import router as bots_router
from .crud.router import router as crud_router

router = APIRouter()

# Addinf router
router.include_router(bots_router)
router.include_router(crud_router)

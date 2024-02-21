# Standard library
from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI

# Utils
from utils.start_server import bot_set_webhook

# Router
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establece el endpoint para telegram
    await bot_set_webhook()
    yield


# API
app = FastAPI(title="Tláloc Bot", lifespan=lifespan)
app.include_router(router)

# Standard library
from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI

# * Routers
from routers import router

# Environment variables
from config import administrator

# Utils
from utils.start_server import sign_up_bots

# Databases
# * related to bot database
from models import metadata_bots
from config import engine_db_bots, database_bots

# * related to Hic Cibus database
metadata_bots.create_all(engine_db_bots)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to Database
    await database_bots.connect()
    await sign_up_bots()
    yield
    # Disconnect from the database
    await database_bots.disconnect()


app = FastAPI(title="API CRUD - HiC Cibus", lifespan=lifespan)
app.include_router(router)

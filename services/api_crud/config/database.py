# Databases
# --// Permite hacer  peticiones asincronas a Database
from databases import Database

# SQLAlchemy
# --// Permite la interacción con la base de datos SQL
from sqlalchemy import create_engine, MetaData

# Environment Variables
from .constans import DB_API_CRUD_URL, DB_BOTS_URL

# Database related to API_CRUD service
engine_db_api_crud = create_engine(DB_API_CRUD_URL, echo=True)
metadata_api_crud = MetaData()
database_api_crud = Database(DB_API_CRUD_URL)

# Database related to bots services
engine_db_bots = create_engine(DB_BOTS_URL, echo=True)
metadata_bots = MetaData()
database_bots = Database(DB_BOTS_URL)

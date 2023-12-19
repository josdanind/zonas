# Databases
# --// Permite hacer  peticiones asincronas a Database
from databases import Database

# SQLAlchemy
# --// Permite la interacción con la base de datos SQL
from sqlalchemy import create_engine, MetaData

# Environment Variables
from .constans import DB_HIC_CIBUS_URL, DB_BOTS_URL

# Database related to API_CRUD service
engine_db_hic_cibus = create_engine(DB_HIC_CIBUS_URL, echo=True)
metadata_hic_cibus = MetaData()
database_hic_cibus = Database(DB_HIC_CIBUS_URL)

# Database related to bots services
engine_db_bots = create_engine(DB_BOTS_URL, echo=True)
metadata_bots = MetaData()
database_bots = Database(DB_BOTS_URL)

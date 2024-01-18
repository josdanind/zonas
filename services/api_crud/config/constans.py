# Standard Library
from os import environ

# Schema
from schemas import CrudUserInDB

# *************************
# * Environment Variables *
# *************************
# * development environment
MODE: bool = environ["DEVELOPMENT_MODE"]

# * Databases
DB_HIC_CIBUS_URL: str = environ["DB_HIC_CIBUS_URL"]
DB_BOTS_URL: str = environ["DB_BOTS_URL"]

# * Admin user
administrator = CrudUserInDB(
    **{
        "username": environ["ADMIN_USERNAME"],
        "email": environ["ADMIN_EMAIL"],
        "password": environ["ADMIN_PASSWORD"],
        "data": {
            "is_superuser": True,
            "full_name": environ["ADMIN_NAME"],
            "scopes": ["admin"],
        },
    }
)

# * JWT config
SECRET_KEY: str = environ["SECRET_KEY"]
ALGORITHM: str = environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS: int = int(environ["ACCESS_TOKEN_EXPIRE_DAYS"])

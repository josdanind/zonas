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
DB_API_CRUD_URL: str = environ["DB_API_CRUD_URL"]
DB_BOTS_URL: str = environ["DB_BOTS_URL"]

# * Admin user
administrator: dict = CrudUserInDB(
    **{
        "username": environ["ADMIN_USERNAME"],
        "email": environ["ADMIN_EMAIL"],
        "password": environ["ADMIN_PASSWORD"],
        "data": {
            "is_superuser": True,
            "name": environ["ADMIN_NAME"],
            "roles": ["admin"],
        },
    }
).model_dump(by_alias=True)

# FastAPI
from fastapi import HTTPException, status

# Utils
from utils.console_message import *

# Databases
from databases import Database

# SQLAlchemy
from sqlalchemy import Table

# library utilities
from .utils import *


class CRUDManager:
    def __init__(self, db: Database, table: Table) -> None:
        self.db = db
        self.db_table = table
        self.table_name = table.name

    async def record(self, record: dict | list):
        try:
            if isinstance(record, dict):
                query = self.db_table.insert().values(**record)
                id = await self.db.execute(query)
                return id
            elif isinstance(record, list):
                query = self.db_table.insert()
                await self.db.execute_many(query, record)
            else:
                raise TypeError("CRUDService.record() expects a list or a dictionary")
        except TypeError as err:
            raise

    @ensure_kwargs_count
    async def verify_existence(
        self, error_message=None, error_if_exist=False, **condition
    ):
        try:
            c_name, c_value = take_first_pair(condition)

            query = self.db_table.select().where(
                eval(f"self.db_table.c.{c_name}") == c_value
            )

            result = await self.db.fetch_one(query)

            if error_if_exist and result:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=error_message
                )

            return result
        except AttributeError as err:
            print_error_message(
                f"No existe el atributo {err} en la tabla {self.table_name}"
            )

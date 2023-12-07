# FastAPI
from fastapi import HTTPException, status

# Utils
from utils.console_message import *

# Databases
from databases import Database

# SQLAlchemy
from sqlalchemy import Table, select, delete

# library utilities
from .utils import *


class CRUDManager:
    def __init__(self, db: Database, table: Table) -> None:
        self.db = db
        self.db_table = table
        self.table_name = table.name

    # **********
    # * Insert *
    # **********
    async def select_all(self):
        """
        Recupera todos los registros en la tabla especificada
        en CRUDManager.

        Returns:
        - Record (Databases): Todos los registros de la tabla.
        """
        return await self.db.fetch_all(select(self.db_table))

    async def select_by_keywords(
        self,
        c_name: str,
        keyword: str | None = None,
        keyword_list: list | None = None,
    ):
        """
        Realiza una consulta asincrónica a la base de datos para seleccionar registros
        con base a un valor de palabra clave o una lista de palabras clave.

        Args:
            c_name (str):  El nombre de la columna en la que buscar.
            keyword (str | None, optional): Una palabra clave única para buscar en la columna especificada.
            keyword_list (list | None, optional): Una lista de palabras clave para buscar en la columna especificada.
        """
        try:
            if keyword == None and keyword_list == None:
                raise TypeError(
                    "CRUDService.select_by_keywords() requires at least one non-empty argument: 'keyword' or 'keyword_list'."
                )
            if keyword_list is not None and keyword is None:
                query = select([self.db_table]).where(
                    eval(f"self.db_table.c.{c_name}.in_({keyword_list})")
                )
            else:
                query = select([self.db_table]).where(
                    eval(f"self.db_table.c.{c_name}") == keyword
                )

            return await self.db.fetch_all(query)
        except TypeError as err:
            print_error_message(err)
        except AttributeError as err:
            print_error_message(
                f'La columna referenciada "{err}" no se encuentra en la tabla "{self.table_name}". '
            )
            raise

    async def select_by_keywords_in_a_list(self, c_name: str, filter_terms: list[str]):
        """
        Esta función realiza un filtrado en la base de datos, buscando registros
        en los cuales la columna especificada almacena una lista de términos
        (strings). Compara cada lista en esta columna con la lista de términos
        de filtro proporcionada. Si algún término de la lista de la columna
        coincide con al menos un término de la lista de filtros, el registro
        correspondiente se incluye en el resultado. Esta funcionalidad es
        especialmente útil para identificar y extraer registros que contengan
        ciertas palabras clave o frases dentro de listas almacenadas en la base
        de datos."

        Args:
        - c_name (str): Nombre de la columna que contiene la lista de string.
        - filter_terms (list[str]): Lista de cadenas de texto usadas para filtrar
        los registros.

        Returns:
            Record: lista de registros devuelto por la la librería Databases
        """
        query = select(self.db_table).where(
            eval(f"self.db_table.c.{c_name}.op('&&')({filter_terms})")
        )

        return await self.db.fetch_all(query)

    # **********
    # * Insert *
    # **********
    async def insert(self, record: dict | list):
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

    # **********
    # * Delete *
    # **********
    async def delete_by_keywords(
        self,
        c_name: str,
        keyword: str | None = None,
        keyword_list: list | None = None,
    ):
        """
        Este método elimina registros donde la columna especificada por `c_name`
        coincide con una `keyword` individual o cualquier palabra clave en
        `keyword_list`. Se debe proporcionar al menos uno de los dos: `keyword` o `keyword_list`.

        Args:
        - c_name (str): Nombre de la columna en la tabla de la base de datos para
        hacer la coincidencia.
        - keyword (str | None, optional): Una única palabra clave para la coincidencia.
        Por defecto es None.
        - keyword_list (list | None, optional):  Una lista de palabras clave para la coincidencia.
        Por defecto es None.
        """
        try:
            if keyword == None and keyword_list == None:
                raise TypeError(
                    "CRUDService.select_by_keywords() requires at least one non-empty argument: 'keyword' or 'keyword_list'."
                )
            if keyword_list is not None and keyword is None:
                query = delete(self.db_table).where(
                    eval(f"self.db_table.c.{c_name}.in_({keyword_list})")
                )
            else:
                query = delete(self.db_table).where(
                    eval(f"self.db_table.c.{c_name}") == keyword
                )

            return await self.db.execute(query)
        except TypeError as err:
            print_error_message(err)
        except AttributeError as err:
            print_error_message(
                f"No existe el atributo {err} en la tabla {self.table_name}"
            )
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

    # **********
    # * Update *
    # **********
    @ensure_kwargs_count
    async def update(self, to_update: dict, **condition):
        try:
            c_name, c_value = take_first_pair(condition)
            no_null_values = {k: v for k, v in to_update.items() if v is not None}

            updated_at = no_null_values.pop("updated_at", False)

            if not no_null_values:
                raise TypeError("CRUDManager.update() expects a non-empty dictionary")

            if updated_at:
                no_null_values["updated_at"] = updated_at

            query = self.db_table.update(
                eval(f"self.db_table.c.{c_name}") == c_value
            ).values(**no_null_values)

            await self.db.execute(query)
            database_message(f"Bot actualizado")

        except TypeError as err:
            print_error_message(err)
            raise

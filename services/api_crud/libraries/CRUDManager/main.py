# FastAPI
from fastapi import HTTPException, status

# Utils
from utils.console_message import *

# Databases
from databases import Database
from databases.backends.postgres import Record

# SQLAlchemy
from sqlalchemy import Table, select, delete, and_
from sqlalchemy.exc import NoSuchColumnError
import sqlalchemy

# library utilities
from .utils import *


class CRUDManager:
    def __init__(self, db: Database, table: Table) -> None:
        self.db = db
        self.db_table = table
        self.table_name = table.name

    async def change_table(self, model: Table):
        self.db_table = model
        self.table_name = model.name

    # **********
    # * Select *
    # **********
    async def select_all(self):
        """
        Recupera todos los registros en la tabla especificada
        en CRUDManager.

        Returns:
        - Record (Databases): Todos los registros de la tabla.
        """
        return await self.db.fetch_all(select(self.db_table))

    async def select_and(
        self,
        fetch_one: bool = True,
        **conditions: dict[str, any]
    )-> Record | list[Record] | None:
        """
        Realiza una consulta SELECT en la tabla asociada, aplicando condiciones
        específicas en la cláusula WHERE.

        Este método permite filtrar registros en la tabla utilizando condiciones
        de tipo `AND`, donde cada clave en `conditions` representa una columna y
        su valor correspondiente es el valor que debe cumplir esa columna.

        Args:
            fetch_one (bool, optional): Indica si se debe devolver solo un
                registro (`True`) o todos los registros que coincidan con las
                condiciones (`False`). Por defecto es `True`.
            **conditions: Claves que representan nombres de columnas y valores
                que representan los valores que se desean filtrar. Por ejemplo,
                `name="John", age=30`.

        Raises:
            NoSuchColumnError: Si se proporciona un nombre de columna en
                `conditions` que no existe en la tabla, se lanza esta excepción
                con un mensaje indicando las columnas inválidas.

        Returns:
            Record | list[Record] | None: Si `fetch_one` es `True`, devuelve
                un objeto de tipo `Record` que representa un solo registro o
                `None` si no se encuentra ningún registro. Si `fetch_one`
                es `False`, devuelve una lista de objetos `Record`, cada uno
                representando un registro.
        """

        query = self.db_table.select()

        # Validar si todas las columnas existen en la tabla
        columns = self.db_table.c.keys()
        invalid_columns = [key for key in conditions if key not in columns]

        if invalid_columns:
            raise NoSuchColumnError(
                f"Las siguientes columnas no existen en la tabla: {', '.join(invalid_columns)}"
            )

        # Añadir condiciones al query
        if conditions:
            conditions_list = [self.db_table.c[key] == value for key, value in conditions.items()]
            query = query.where(and_(*conditions_list))

        # Ejecutar la consulta
        return await self.db.fetch_one(query) if fetch_one else await self.db.fetch_all(query)

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

            # Número de filas actualizadas
            updated_rows = await self.db.execute(
                self.db_table.select()
                .where(eval(f"self.db_table.c.{c_name}") == c_value)
                .with_only_columns([sqlalchemy.func.count()])
            )

            return updated_rows
        except TypeError as err:
            print_error_message(err)
            raise

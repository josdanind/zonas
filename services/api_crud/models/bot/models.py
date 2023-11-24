# SQLAlchemy
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    TEXT,
)
from sqlalchemy.dialects.postgresql import ARRAY


def createBotModel(metadata: MetaData) -> Table:
    """Crea y retorna la tabla `bots` utilizando el
    objeto MetaData proporcionado.

    La tabla creada incluirá las siguientes columnas:
    - `bot_id (int)`: Identificador único para cada bot, actúa como primary_key
    - `name (str)`: Nombre único para cada bot, requerido para acceder a la CRUD.
    - `category (list[str])`: Categorías a la que pertenece el bot.
    - `hashed_password (str)`: Representación cifrada de la contraseña del bot.
    - `description (str)`: Descripción del bot.
    - `is_active (bool)`: Bool que representa si el bot está activo.
    - `created_at (DateTime)`: Fecha y hora en que se creó el registro del bot, generada automáticamente.
    - `updated_at (DateTime)`: Fecha y hora de la última actualización del registro del bot.

    Args:
    - `metadata (MetaData)`: Un objeto MetaData, vincula la tabla `bots`.

    Returns:
    - `Table (Table):` Objeto Table de SQLAlchemy que representa la estructura de la tabla `bots` en la base de datos.
    """
    return Table(
        "bots",
        metadata,
        Column("bot_id", Integer, primary_key=True),
        Column("name", String(10), unique=True, nullable=False),
        Column("categories", ARRAY(String), nullable=False),
        Column("hashed_password", String, nullable=False),
        Column("description", TEXT),
        Column("is_active", Boolean, default=True),
        Column("created_at", DateTime, default=func.now()),
        Column("updated_at", DateTime),
    )

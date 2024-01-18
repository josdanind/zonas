# Standard Library
from datetime import datetime
from typing import Annotated

# FastAPI
from fastapi import APIRouter, status, HTTPException, Query, Depends

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Database - Databases lib
from config import database_bots

# Schemas
from schemas import BotInfo, KeywordsForDB, DeletedBots, BotInDB, BotInDBUpdate, Token

# Models
from models import botModel, crudUserModel

# Utils
from utils.console_message import *
from utils.jwt_manager import user_authorization

router = APIRouter(prefix="/bots", tags=["Bots"])


# ************
# * GET Bots *
# ************
@router.get(
    path="/get_bots",
    status_code=status.HTTP_200_OK,
    summary="Obtener uno o varios de los bots",
    response_model=list[BotInfo],
    description="""
Este endpoint retorna información sobre uno o más bots utilizados por Hic-cibus.
Puede especificar los nombres de los bots a través del parámetro `bots` en la consulta.

### Uso:
Para obtener información de bots específicos, incluye sus nombres en el parámetro
de consulta `bots`. Puedes especificar múltiples nombres separándolos con `&`.

#### Ejemplos de Consultas:
- Para un único bot: `/get_bots?bots=bot_x`
- Para múltiples bots: `/get_bots?bots=bot_x&bots=bot_y`

### Respuesta:
La respuesta es una lista de objetos `BotResponse`, cada uno conteniendo detalles
del bot solicitado.

### Notas:
- Si no se especifica ningún bot, se retornará información de todos los bots disponibles.
- Asegúrate de que los nombres de los bots estén correctamente escritos para
evitar errores en la consulta.
    """,
)
async def get_bots(
    current_user: Annotated[crudUserModel, Depends(user_authorization)],
    bots: list[str] = Query(
        None, description="Nombres de bots a recuperar de la base de datos."
    ),
):
    crud_manager = CRUDManager(database_bots, botModel)

    if bots is None:
        return await crud_manager.select_all()

    bots_record = await crud_manager.select_by_keywords(
        c_name="name", keyword_list=bots
    )

    return [bot for bot in bots_record]


# ***************
# * Delete Bots *
# ***************
@router.delete(
    path="/delete",
    status_code=status.HTTP_200_OK,
    summary="Eliminar uno o varios bots",
    response_model=DeletedBots,
)
async def delete_bots(
    userRequest: KeywordsForDB,
    current_user: Annotated[crudUserModel, Depends(user_authorization)],
):
    try:
        crud_manager = CRUDManager(database_bots, botModel)

        c_name = userRequest.c_name
        keywords = userRequest.keywords

        existing_bots = await crud_manager.select_by_keywords(
            c_name=userRequest.c_name, keyword_list=userRequest.keywords
        )

        bot_names = [record["name"] for record in existing_bots]

        no_existing_bots = [bot for bot in keywords if bot not in bot_names]

        if bot_names:
            await crud_manager.delete_by_keywords(c_name=c_name, keyword_list=bot_names)
            database_message(f"Bots eliminados: {','.join(bot_names)}")
        return DeletedBots(
            eliminated=len(bot_names),
            delete_bot=bot_names,
            non_existent_bots=no_existing_bots,
        )
    except AttributeError as err:
        error_message = f"No existe la columna '{err}' en la tabla bots"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_message)


# ***************
# * Insert Bots *
# ***************
@router.post(
    path="/insert",
    status_code=status.HTTP_200_OK,
    summary="Crear un bot",
)
async def delete_bots(
    userRequest: BotInDB,
    current_user: Annotated[crudUserModel, Depends(user_authorization)],
):
    crud_manager = CRUDManager(database_bots, botModel)

    bot_dict = userRequest.model_dump(by_alias=True)
    bot_name = bot_dict["name"]

    await crud_manager.verify_existence(
        f"El bot '{bot_name}' ya existe.", True, name=bot_name
    )

    await crud_manager.insert(bot_dict)
    database_message(f"Bot {bot_name} was created")

    return {"message": f"Bot {bot_name} was created"}


# **************
# * Update Bot *
# **************
@router.put(
    path="/update",
    status_code=status.HTTP_200_OK,
    summary="Actualizar bot",
)
async def delete_bots(
    id: int,
    userRequest: BotInDBUpdate,
    current_user: Annotated[crudUserModel, Depends(user_authorization)],
):
    try:
        crud_manager = CRUDManager(database_bots, botModel)
        exists = await crud_manager.verify_existence(bot_id=id)

        if exists:
            to_update = userRequest.model_dump(by_alias=True)
            to_update["updated_at"] = datetime.now()

            await crud_manager.update(to_update, bot_id=id)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Se espera un json no vacio"
        )

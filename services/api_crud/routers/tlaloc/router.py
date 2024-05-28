# Standard Library
from typing import Annotated
from datetime import datetime

# FastAPI
from fastapi import APIRouter, status, Path, HTTPException, Query

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Database - Databases lib
from config import database_hic_cibus

# Models
from models import sessionModel

# Schemas
from schemas import UserLoginSchema, RequestToUpdateSessionSchema, SessionInDBUpdate

router = APIRouter(prefix="/tlaloc", tags=["Tlaloc"])


# ********************
# * POST - Bot Login *
# ********************
@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Autenticación de Usuarios",
)
async def bot_user_auth(
    userRequest: UserLoginSchema,
):
    username = userRequest.username
    chat_id = userRequest.chat_id

    crud_manager = CRUDManager(database_hic_cibus, sessionModel)

    query = """\
    SELECT
        sessions.id AS session_id,
        sessions.main_message_id,
        sessions.current_action,
        sessions.chat_id,
        workers.id AS worker_id,
        workers.name
    FROM
        sessions
    JOIN
        workers ON sessions.worker_id = workers.id
    WHERE
        sessions.telegram_user = :username;
    """

    user = await crud_manager.db.fetch_one(query, {"username": username})

    if user:
        if not user.chat_id:
            to_update = SessionInDBUpdate(chat_id=chat_id).model_dump(exclude_none=True)
            to_update["updated_at"] = datetime.now()

            await crud_manager.update(to_update, telegram_user=username)

        return {
            "worker_id": user.worker_id,
            "chat_id": user.chat_id,
            "name": user.name,
            "session_id": user.session_id,
            "main_message_id": user.main_message_id,
            "current_action": user.current_action,
        }

    else:
        raise HTTPException(status_code=404, detail="The user does not exist")


# ************************
# * PUT - Update Session *
# ************************
@router.put(
    path="/update_session",
    status_code=status.HTTP_200_OK,
    summary="Administra las sesiones de los usuarios",
)
async def update_worker_session(userRequest: RequestToUpdateSessionSchema):
    crud_manager = CRUDManager(database_hic_cibus, sessionModel)

    session_id = userRequest.session_id
    to_update = userRequest.session_table.model_dump(exclude_none=True)
    to_update["updated_at"] = datetime.now()

    result = await crud_manager.update(to_update, id=session_id)

    return result

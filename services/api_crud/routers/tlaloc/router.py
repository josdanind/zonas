# Standard Library
from typing import Annotated

# FastAPI
from fastapi import APIRouter, status, Path, HTTPException

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Database - Databases lib
from config import database_hic_cibus

# Models
from models import workerModel, sessionModel

# Schemas
from schemas import SessionInDBUpdate

router = APIRouter(prefix="/tlaloc", tags=["Tlaloc"])


# ********************
# * POST - Bot Login *
# ********************
@router.get(
    path="/login/{username}",
    status_code=status.HTTP_200_OK,
    summary="Autenticación de Usuarios",
)
async def bot_user_auth(username: Annotated[str, Path(title="Telegram Username")]):
    crud_manager = CRUDManager(database_hic_cibus, workerModel)

    query = f"""\
    SELECT
        workers.id AS worker_id,
        workers.chat_id,
        workers.name,
        sessions.id AS session_id,
        sessions.main_message_id,
        sessions.current_action
    FROM
        workers
    JOIN
        sessions ON workers.id = sessions.worker_id
    WHERE
        workers.telegram_user = '{username}';
    """

    user = await crud_manager.db.fetch_one(query)

    if user:
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
async def update_worker_session(session_id: int, userRequest: SessionInDBUpdate):
    crud_manager = CRUDManager(database_hic_cibus, sessionModel)
    exists = await crud_manager.verify_existence(id=session_id)

    # crud_manager.verify_existence(telegram_user=username)

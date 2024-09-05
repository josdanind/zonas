# Standard Library
from datetime import datetime

# FastAPI
from fastapi import HTTPException

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Databases
from config import database_hic_cibus

# Schemas
from schemas import UserLoginSchema, SessionInDBUpdateSchema

# Models
from models import sessionModel



async def login(
    credentials: UserLoginSchema,
    error_message: str
):
    username = credentials.username
    chat_id = credentials.chat_id

    crud_manager = CRUDManager(database_hic_cibus, sessionModel)

    query = """\
    SELECT
        sessions.id AS session_id,
        sessions.main_message_id,
        sessions.current_action,
        sessions.chat_id,
        workers.id AS worker_id,
        workers.name,
        farms.id AS farm_id
    FROM
        sessions
    JOIN
        workers ON sessions.worker_id = workers.id
    JOIN
        farms ON workers.farm_id = farms.id
    WHERE
        sessions.telegram_user = :username;
    """

    user = await crud_manager.db.fetch_one(query, {"username": username})

    if user:
        if not user.chat_id:
            to_update = SessionInDBUpdateSchema(chat_id=chat_id).model_dump(exclude_none=True)
            to_update["updated_at"] = datetime.now()
            await crud_manager.update(to_update, telegram_user=username)

        return {
            "worker_id": user.worker_id,
            "chat_id": user.chat_id,
            "name": user.name,
            "session_id": user.session_id,
            "main_message_id": user.main_message_id,
            "current_action": user.current_action,
            "physical_frames": user.physical_frames,
            "farm_id": user.farm_id
        }

    else:
        raise HTTPException(status_code=404, detail=error_message)

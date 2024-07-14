# Pydantic
from pydantic import BaseModel


class SessionInDBSchema(BaseModel):
    id: int | None = None
    worker_id: int
    telegram_user: str
    chat_id: int | None = None
    main_message_id: int | None = None
    current_action: dict | None = None


class SessionInDBUpdateSchema(BaseModel):
    worker_id: int | None = None
    telegram_user: str | None = None
    chat_id: int | None = None
    main_message_id: int | None = None
    current_action: dict | None = None


class RequestToUpdateSessionSchema(BaseModel):
    session_id: int
    session_table: SessionInDBUpdateSchema

# Pydantic
from pydantic import BaseModel


class WorkerData(BaseModel):
    email: str
    tasks: dict


class WorkerInDB(BaseModel):
    id: int | None = None
    farm_id: int
    name: str
    telegram_user: str
    chat_id: int | None = None
    photography: bytes | None = None
    contact: str | None = None
    is_active: bool | None = None
    position: list[str]
    data: WorkerData

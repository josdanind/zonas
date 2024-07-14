# Pydantic
from pydantic import BaseModel
from uuid import UUID


class ControlSystemInDB(BaseModel):
    id: int | None = None
    crop_id: int
    uuid: UUID
    device: str
    description: str
    categories: list[str]
    frame: dict
    data: dict

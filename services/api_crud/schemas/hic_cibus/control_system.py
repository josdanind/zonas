# Pydantic
from pydantic import BaseModel
from uuid import UUID


class ControlSystemData(BaseModel):
    controller: dict


class ControlSystemInDB(BaseModel):
    id: int | None = None
    crop_id: int
    uuid: UUID
    device: str
    description: str
    categories: list[str]
    data: ControlSystemData

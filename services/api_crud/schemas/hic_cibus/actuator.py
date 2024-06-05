# Pydantic
from pydantic import BaseModel
from typing import Dict, Any


class ActuatorData(BaseModel):
    marker: str
    control_type: str
    extra_data: Dict[str, Any] = {}


class ActuatorInDB(BaseModel):
    id: int | None = None
    uuid: str
    controller_id: int
    ref: str
    description: str
    categories: list[str]
    data: ActuatorData

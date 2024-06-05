# Pydantic
from pydantic import BaseModel
from typing import Dict, Any


class SensorData(BaseModel):
    marker: str
    control_type: str
    extra_data: Dict[str, Any] = {}


class SensorInDB(BaseModel):
    id: int | None = None
    uuid: str
    controller_id: int
    ref: str
    description: str
    quantity: list[str]
    data: SensorData

from datetime import datetime

# Pydantic
from pydantic import BaseModel
from typing import Dict, Any

class SensorData(BaseModel):
    marker: str
    control_type: str
    extra_data: Dict[str, Any] = {}

class SensorLogs(BaseModel):
    sensor_id: int
    timestamp: datetime
    quantity: str
    unit: str
    value: float

class SensorInDB(BaseModel):
    id: int | None = None
    uuid: str
    controller_id: int
    ref: str
    description: str
    quantity: list[str]
    data: SensorData

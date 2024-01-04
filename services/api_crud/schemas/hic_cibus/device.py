# Pydantic
from pydantic import BaseModel


class DeviceData(BaseModel):
    marker: str


class DeviceInDB(BaseModel):
    id: int | None = None
    control_system_id: int
    uuid: str
    ref: str
    control_type: str
    description: str
    categories: list[str]
    data: DeviceData

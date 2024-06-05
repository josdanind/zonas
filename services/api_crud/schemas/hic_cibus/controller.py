# Pydantic
from pydantic import BaseModel


class ControllerInDB(BaseModel):
    id: int | None = None
    uuid: str
    control_system_id: int
    device: str
    description: str
    data: dict

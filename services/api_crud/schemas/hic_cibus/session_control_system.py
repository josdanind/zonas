# Pydantic
from pydantic import BaseModel


class SessionControlSystemInDB(BaseModel):
    id: int | None = None
    session_id: int
    control_system_id: int

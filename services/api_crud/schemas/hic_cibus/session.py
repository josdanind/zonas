# Pydantic
from pydantic import BaseModel


class SessionInDB(BaseModel):
    id: int | None = None
    worker_id: int
    main_message_id: int | None = None
    current_action: dict | None = None

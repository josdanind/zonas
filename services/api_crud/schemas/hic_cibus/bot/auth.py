# Pydantic
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    chat_id: int

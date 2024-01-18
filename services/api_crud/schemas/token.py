# Pydantic
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    id: int
    username: str
    scopes: list[str] = []

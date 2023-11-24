# Pydantic
from pydantic import BaseModel, constr, EmailStr, validator, Field

# Utils
from utils.encrypt import context


class BotInDB(BaseModel):
    name: str
    categories: list[str]
    password: str = Field(serialization_alias="hashed_password")
    description: str | None = None
    is_active: bool = True

    @validator("password")
    def hash_password(cls, password):
        return context.hash(password)

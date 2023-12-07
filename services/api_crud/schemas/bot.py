# Pydantic
from pydantic import BaseModel, validator, Field, root_validator

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

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "robot-name",
                "categories": ["IA", "Trading"],
                "password": "password_123",
                "description": "Es un bot para hacer trading",
                "is_active": True,
            }
        }
    }


class BotInDBUpdate(BaseModel):
    name: str | None = None
    categories: list[str] | None = None
    password: str | None = Field(default=None, serialization_alias="hashed_password")
    description: str | None = None
    is_active: bool | None = None

    @validator("password")
    def hash_password(cls, password):
        return context.hash(password)


class BotInfo(BaseModel):
    bot_id: int
    name: str
    is_active: bool


class DeletedBots(BaseModel):
    eliminated: int
    delete_bot: list
    non_existent_bots: list

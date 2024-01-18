# Pydantic
from pydantic import BaseModel, constr, EmailStr, validator, Field

# Utils
from utils.encrypt import context


class DataSchema(BaseModel):
    is_superuser: bool = False
    full_name: constr(min_length=3, max_length=100)
    scopes: list = ["user"]


class CrudUserInDB(BaseModel):
    username: constr(min_length=3, max_length=100)
    email: EmailStr
    disabled: bool = False
    password: str = Field(serialization_alias="hashed_password")
    data: DataSchema

    @validator("password")
    def hash_password(cls, password):
        return context.hash(password)

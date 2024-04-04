# Pydantic
from pydantic import BaseModel, validator, FilePath


class ButtonSchema(BaseModel):
    display_name: str
    callback_data: str


class FrameWithImageSchema(BaseModel):
    cover_path: FilePath
    title: str
    description: str
    buttons: list[ButtonSchema]

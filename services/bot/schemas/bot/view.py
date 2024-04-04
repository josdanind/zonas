# Standard Library
from typing import Optional

# Pydantic
from pydantic import BaseModel


class ViewSchema(BaseModel):
    name: str
    callback_data: str
    path: str
    back_button: bool
    cover: str


class MainViewSchema(ViewSchema):
    # callback_data: Optional[None] = Field(default=None, exclude=True)
    buttons: dict[str, dict]
    api_crud_url: str


class ViewBuilderSchema(ViewSchema):
    pass

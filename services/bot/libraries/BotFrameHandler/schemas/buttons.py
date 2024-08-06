# Pydantic
from pydantic import BaseModel


class ButtonSchema(BaseModel):
    text: str
    callback_data: str

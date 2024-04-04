# pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup

# Pydantic
from pydantic import BaseModel, validator, ConfigDict


# Esquemas que representan al "frontend" de cada View
class viewFrontend_Schema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    cover: str
    path: str
    keyboard: InlineKeyboardMarkup

    @validator("keyboard", pre=True)
    def check_keyboard(cls, v):
        if not isinstance(v, InlineKeyboardMarkup):
            raise ValueError("keyboard must be an InlineKeyboardMarkup instance")
        return v


# Esquema que representa el "frontend" de la Main View
class homeFrontend_Schema(viewFrontend_Schema):
    name: str = "Home"


# Esquema que representa un objeto View
class ViewSchema(BaseModel):
    name: str
    callback_data: str
    path: str
    back_button: bool
    cover: str


class MainViewSchema(ViewSchema):
    buttons: dict[str, dict]
    api_crud_url: str

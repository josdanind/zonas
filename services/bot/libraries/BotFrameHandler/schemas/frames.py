# Standard Library
from typing import Literal

# Pydantic
from pydantic import BaseModel, Field, ConfigDict

from telebot.types import InlineKeyboardMarkup

#! cambiar nombre frame_template -> template
class FrameSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cover: bytes | str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    caption: str | None = None
    parse_mode: str | None = None
    frame_template: str = "with_cover"

class FrameWithCoverSchema(FrameSchema):
    cover: bytes | str
    row_width: Literal[1] = 1

class PhysicalFrame(BaseModel):
    #! Preguntar que es
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int | None = None
    theater: str | None = None
    cover: bytes | str | None = None
    buttons: list | None = None
    caption: str | None = None
    template: str = "with_cover"
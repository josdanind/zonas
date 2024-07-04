# Standard Library
from typing import Literal

# Pydantic
from pydantic import BaseModel, Field, ConfigDict

from telebot.types import InlineKeyboardMarkup

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
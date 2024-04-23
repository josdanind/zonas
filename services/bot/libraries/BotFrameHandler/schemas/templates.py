# Standard Library
from typing import Literal

# Pydantic
from pydantic import BaseModel, Field, ConfigDict

from telebot.types import InlineKeyboardMarkup


class FrameWithImageSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    photo: bytes
    reply_markup: InlineKeyboardMarkup | None = None
    caption: str | None = None
    parse_mode: str | None = None
    template_name: Literal["whit_img"] = "whit_img"

# Standard Library
import os

# BOT
from ..config.bot import bot

# BotFrameHandler
from libraries.BotFrameHandler import TheaterHandler

# ************
# * THEATERS *
# ************
from .theaters.orchards.theater import theater as orchard_theater

current_dir = os.path.dirname(os.path.abspath(__file__))

text_box = {"title": "Bienvenidos a Tlaloc", "description": "Selecciona un proceso"}

theater_handler = TheaterHandler(
    bot=bot, theaters=[orchard_theater], path=current_dir, text_box=text_box
)

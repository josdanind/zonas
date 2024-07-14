# Standard Library
import os

# Environment Variables
from config import API_CRUD_URL

# BOT
from ..config.bot import bot

# BotFrameHandler
from libraries.BotFrameHandler import TheaterHandler

# ************
# * THEATERS *
# ************
from .theaters.orchards.theater import theater as orchard_theater

current_dir = os.path.dirname(os.path.abspath(__file__))

text_box = {"title": "Bienvenido a Tlaloc", "description": "Selecciona un proceso"}

theater_handler = TheaterHandler(
    bot=bot,
    theaters=[orchard_theater],
    path=current_dir,
    text_box=text_box,
    api_crud_url=API_CRUD_URL,
)
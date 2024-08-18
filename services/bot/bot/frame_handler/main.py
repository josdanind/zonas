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

# URL donde se aloja la imagen del cover
COVER_URL = "https://imgur.com/9Ng2xrK"

# Text box, texto descriptivo del Frame del TheaterHandler (lobby)
text_box = {
    "title": "Bienvenido a Tlaloc",
    "description": "Selecciona un proceso"
}

theater_handler = TheaterHandler(
    bot=bot,
    theaters=[orchard_theater],
    cover_url=COVER_URL,
    text_box=text_box,
    api_crud_url=API_CRUD_URL,
)
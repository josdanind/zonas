# config
from config import metadata_api_crud, metadata_bots

# Model templates
from .bot.models import createBotModel

# Bots
botModel = createBotModel(metadata_bots)

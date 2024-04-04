# Standard Library
import os

# Environment Variable
from config import API_CRUD_URL

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import set_container_settings

container_path = os.path.dirname(os.path.abspath(__file__))

# *********
# *  View *
# *********
frame = set_container_settings(container_path)

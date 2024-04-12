# Standard Library
import os

# Environment Variable
from config import API_CRUD_URL

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import create_TheaterSchema

container_path = os.path.dirname(os.path.abspath(__file__))

# *********
# *  View *
# *********
theater = create_TheaterSchema(container_path)

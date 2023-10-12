# Bot container environment variables
from os import environ

# *************************
# * Environment Variables *
# *************************

DEVELOPMENT_MODE = True if environ["DEVELOPMENT_MODE"] == "true" else False
BOT_TOKEN = environ["BOT_TOKEN"]
NGROK_TOKEN = environ["NGROK_TOKEN"]
BOT_DOMAIN = environ["BOT_DOMAIN"]

# Bot
from bot import bot

# Environment variables
from config import NGROK_TOKEN, DEVELOPMENT_MODE, BOT_DOMAIN

# Utils
from .ngrok import init_ngrok


async def bot_set_webhook():
    if DEVELOPMENT_MODE:
        # Development domain
        app_url = init_ngrok(NGROK_TOKEN)
    else:
        # Production domain
        app_url = BOT_DOMAIN

    # Webhook endpoint
    app_url += "/webhook"
    await bot.set_webhook(app_url)

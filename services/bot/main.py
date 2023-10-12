# FastAPI
from fastapi import FastAPI

# Utils
from utils.ngrok import init_ngrok

# Environment variables
from config import NGROK_TOKEN, DEVELOPMENT_MODE, BOT_DOMAIN

# Bot
from bot import bot

# Router
from router import router


# API
app = FastAPI(title="Zonas")
app.include_router(router)


@app.on_event("startup")
async def startup():
    if DEVELOPMENT_MODE:
        # Development domain
        app_url = init_ngrok(NGROK_TOKEN)
    else:
        # Production domain
        app_url = BOT_DOMAIN

    # Webhook endpoint
    app_url += "/webhook"

    # Set the webhook to receive Telegram updates and messages
    await bot.set_webhook(app_url)

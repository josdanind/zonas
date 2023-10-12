# Standard Library
import json

# FastAPI
from fastapi import APIRouter, status, Request, HTTPException

# pyTelegramBotAPI
import telebot.async_telebot as telebot

# Bot
from bot import bot

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    if request.headers["content-type"] == "application/json":
        try:
            data = await request.json()

            async_update = telebot.types.Update.de_json(json.dumps(data))

            await bot.process_new_updates([async_update])

        except Exception as e:
            print("Error enviando actualizaciones al objeto update del Bot.")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Header inválido, no se puede procesar el update del Bot",
        )

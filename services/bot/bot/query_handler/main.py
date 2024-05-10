# Standard library
import re

# BOT
from ..config.bot import bot
from telebot.types import CallbackQuery

# Frame Handler
from ..frame_handler.main import theater_handler

# Utils - BotFrameHandler
from libraries.BotFrameHandler.utils import print_test
from ..frame_handler.main import theater_handler


# ********************
# * Button - Go Back *
# ********************
@bot.callback_query_handler(func=lambda call: "goBack" in call.data)
async def goBack_button(call: CallbackQuery):
    chat_id = call.from_user.id
    username = call.from_user.username
    frame = re.search(r"@(.+)", call.data).group(1)

    if frame == "lobby":
        await theater_handler.send_frame(theater_handler.lobby_frame, chat_id)

    await bot.answer_callback_query(call.id)


# ******************************
# * Button - Redirect To Frame *
# ******************************
@bot.callback_query_handler(func=lambda call: "@" in call.data)
async def redirect_to_frame_button(call: CallbackQuery):
    try:
        chat_id = call.from_user.id
        username = call.from_user.username

        theater = re.search(r"@(.*?)://", call.data).group(1)
        gallery = re.search(r"://(.*?)$", call.data).group(1)

        if gallery == "galleries":
            lobby_frame = theater_handler.frames[theater]["frame"]
            await theater_handler.send_frame(lobby_frame, chat_id)

        await bot.answer_callback_query(call.id)
    except Exception as e:
        #! IMPLEMENTAR EXCEPCIÓN
        print("Ocurrrio un error", e)

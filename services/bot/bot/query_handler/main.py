# Standard library
import re

# BOT
from ..config.bot import bot
from telebot.types import CallbackQuery
from ..utils.bot_api import authenticate_user, update_session

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

    user = await authenticate_user(username, chat_id)

    if frame == "lobby":
        await theater_handler.change_message(
            chat_id=chat_id,
            message_id=user["main_message_id"],
            frame=theater_handler.lobby_frame,
        )

    await bot.answer_callback_query(call.id)


# ******************************
# * Button - Redirect To Frame *
# ******************************
@bot.callback_query_handler(func=lambda call: "@" in call.data)
async def redirect_to_frame_button(call: CallbackQuery):
    try:
        chat_id = call.from_user.id
        username = call.from_user.username

        user = await authenticate_user(username, chat_id)

        theater = re.search(r"@(.*?)://", call.data).group(1)
        gallery = re.search(r"://(.*?)$", call.data).group(1)

        if gallery == "galleries":
            lobby_frame = theater_handler.frames[theater]["frame"]
            await theater_handler.change_message(
                chat_id=chat_id, message_id=user["main_message_id"], frame=lobby_frame
            )

            to_update = {"current_action": {"route": f"/{theater}"}}
            await update_session(user["session_id"], to_update)
            # await theater_handler.send_frame(lobby_frame, chat_id)

        await bot.answer_callback_query(call.id)
    except Exception as e:
        #! IMPLEMENTAR EXCEPCIÓN
        print("Ocurrrio un error", e)

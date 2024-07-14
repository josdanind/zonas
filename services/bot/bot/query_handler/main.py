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

# Utils - Bot
from ..utils.bot_api import get_buttons

# pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment Variables
from config import API_CRUD_URL

# Schemas
from libraries.BotFrameHandler.schemas import FrameSchema

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
    else:
        await theater_handler.change_message(
            chat_id=chat_id,
            message_id=user["main_message_id"],
            frame=theater_handler.frames[frame]["frame"],
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

        theater_data = theater_handler.frames[theater]
        container_url =  API_CRUD_URL + theater_data["container_path"]

        match gallery:
            case "galleries":
                lobby_frame = theater_data["frame"]
                await theater_handler.change_message(
                    chat_id=chat_id, message_id=user["main_message_id"], frame=lobby_frame
                )

                to_update = {"current_action": {"route": f"/{theater}"}}
                # ! aqui devuelve el numero de filas modificadas, si es cero, manejar la excepción 
                await update_session(user["session_id"], to_update)
            case "atrium":
                atrium = theater_data["galleries"]["atrium"]
                atrium_link = atrium["link"]

                # * COVER
                atrium_cover = atrium["cover"]

                # * BUTTONS
                buttons_dict: list = await get_buttons(
                    container_url, atrium_link, atrium["query"], user["farm_id"]
                )

                buttons_dict.append({
                    "text": "Ir atrás",
                    "callback_data": f"goBack@{theater}",
                })

                # * KEYBOARD
                atrium_keyboard = InlineKeyboardMarkup(row_width=1)
                atrium_keyboard.add(
                    *[InlineKeyboardButton(**button) for button in buttons_dict]
                )

                # * CAPTION
                atrium_caption = atrium["text_box"]
                # --// Title
                title = atrium_caption["title"]
                # --// Description
                description = atrium_caption["description"]
                # --// Caption
                caption = f"<b>{title}</b>\n\n{description}"

                atrium_frame = FrameSchema(
                    cover=atrium_cover,
                    reply_markup=atrium_keyboard,
                    caption=caption,
                    parse_mode="HTML"
                )

                await theater_handler.change_message(
                    chat_id=chat_id, message_id=user["main_message_id"], frame=atrium_frame
                )

                to_update = {"current_action": {"route": f"/{theater}/{gallery}"}}
                # ! aqui devuelve el numero de filas modificadas, si es cero, manejar la excepción 
                await update_session(user["session_id"], to_update)
            case _:
                pass

        await bot.answer_callback_query(call.id)
    except Exception as e:
        #! IMPLEMENTAR EXCEPCIÓN
        print("Ocurrrio un error", e)
